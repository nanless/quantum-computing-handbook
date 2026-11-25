#!/usr/bin/env python3
"""Run the book's offline experiments and check source snapshots where included."""
import argparse
import datetime
import json
import os
import pathlib
import platform
import shlex
import subprocess
import sys
import time

from validation_reports import OUTPUT_ENV, ROOT, write_atomic


TIMEOUT_SECONDS = 90
VENDOR_CHECK = ['snapshot_sources.py', '--verify']
RELEASE_MANIFEST = {
    'schema_version': 1,
    'profile': 'authored-code-release',
    'vendor_snapshot': 'excluded',
}
COMMANDS=[['foundations/foundations_lab.py','--case','all'],
 ['foundations/measurement_validation.py'],['foundations/circuit_channel_boundaries.py'],
 ['foundations/hamiltonian_validation.py','--case','all'],
 ['foundations/information_capacity_boundaries.py'],
 ['algorithms/experiments.py','all'],['algorithms/qpe_modular_checks.py'],
 ['systems/hardware_flags.py'],['systems/hardware_readout_boundaries.py'],
 ['systems/weighted_decoder.py'],['systems/factory_schedule.py'],
 ['systems/network_wait.py'],['systems/routing_mapping.py'],['systems/service_timeline.py'],
 ['systems/control_bandwidth.py'],['algorithms/poisson_scalar_baseline.py'],
 ['systems/network_protocol_boundaries.py'],['practice/statistics_boundaries.py'],
 ['systems/stabilizer_distillation_checks.py'],['systems/pauli_benchmark_checks.py'],
 ['algorithms/verification_model_boundaries.py'],['algorithms/application_boundaries.py'],
 ['systems/compilation_boundaries.py'],
 ['foundations/diagnostic_lab.py','--case','all'],['algorithms/round70_checks.py','all'],
 ['foundations/round71_checks.py','--case','all'],['algorithms/round71_checks.py','all'],
 ['systems/round71_checks.py','--case','all'],
 ['foundations/round72_stdlib.py','--case','all'],['algorithms/round72_checks.py','all'],
 ['systems/round72_checks.py','--case','all'],
 ['foundations/round73_checks.py','--case','all'],['algorithms/round73_checks.py','all'],
 ['systems/round73_checks.py','--case','all'],['sdk/round73/check_saved.py'],
 ['review/cross_foundations.py'],['review/cross_systems.py'],
 ['systems/calibration_uncertainty.py'],['systems/coherent_repetition.py'],
 ['systems/correlated_shots.py'],['systems/network_cutoff.py'],
 ['systems/resource_schedule.py'],['systems/calibration_dependencies.py'],
 ['systems/sensing_lab.py'],['algorithms/simulation_engines_lab.py'],
 ['algorithms/v4_algorithms_lab.py','all'],['practice/v4_practice_lab.py'],
 ['practice/source_reading_checks.py'],['practice/experiments.py'],['practice/research_checks.py'],
 ['practice/workflow_checks.py'],VENDOR_CHECK,['tests/test_snapshot_sources.py']]


def validation_profile():
    marker = ROOT / 'CODE-VALIDATION.json'
    source_paths = (ROOT / '.git', ROOT / 'handbook', ROOT / 'AGENTS.md', ROOT / 'codes/vendor')
    if not marker.exists() or any(path.exists() or path.is_symlink() for path in source_paths):
        return 'full-repository'
    if json.loads(marker.read_text(encoding='utf-8')) != RELEASE_MANIFEST:
        raise ValueError(f'Unrecognized standalone release profile: {marker}')
    return RELEASE_MANIFEST['profile']


def timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def output_text(output):
    return output.decode('utf-8', errors='replace') if isinstance(output, bytes) else output or ''


def run_check(args, env):
    command = [sys.executable, str(ROOT / 'codes' / args[0]), *args[1:]]
    record = {
        'command': shlex.join(['python3', f'codes/{args[0]}', *args[1:]]),
        'argv': command,
        'cwd': str(ROOT),
        'timeout_seconds': TIMEOUT_SECONDS,
    }
    started = time.monotonic()
    try:
        run = subprocess.run(
            command, cwd=ROOT, env=env, capture_output=True, encoding='utf-8',
            errors='replace', timeout=TIMEOUT_SECONDS,
        )
        record.update(
            status='passed' if run.returncode == 0 else 'failed',
            returncode=run.returncode, stdout=run.stdout, stderr=run.stderr,
        )
    except subprocess.TimeoutExpired as error:
        record.update(
            status='timed_out', returncode=124, stdout=output_text(error.stdout),
            stderr=output_text(error.stderr), error=f'Exceeded {TIMEOUT_SECONDS} seconds',
        )
    except OSError as error:
        record.update(status='failed', returncode=1, stdout='', stderr=str(error))
    record['elapsed_seconds'] = time.monotonic() - started
    return record


def main(argv=None):
    if not __debug__:
        raise RuntimeError('Run without -O: assertions are part of validation')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=pathlib.Path, default=ROOT / 'work/research',
                        help='Directory for the current suite report and child results')
    options = parser.parse_args(argv)
    destination = options.output_dir.resolve()
    profile = validation_profile()
    env = {**os.environ, OUTPUT_ENV: str(destination / 'local-check-results'),
           'PYTHONDONTWRITEBYTECODE': '1'}
    report = {
        'date_utc': timestamp(),
        'python': platform.python_version(),
        'profile': profile,
        'scope': ('authored stdlib tests and vendor integrity; no upstream execution'
                  if profile == 'full-repository' else
                  'authored stdlib tests; vendor excerpts excluded from the standalone archive'),
        'status': 'running',
        'checks': [],
    }
    report_path = destination / 'code-validation.json'
    write_atomic(report_path, json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    for args in COMMANDS:
        if profile == RELEASE_MANIFEST['profile'] and args == VENDOR_CHECK:
            record = {
                'command': 'python3 codes/snapshot_sources.py --verify',
                'status': 'not_applicable',
                'returncode': None,
                'reason': 'Standalone release metadata declares vendor excerpts excluded.',
            }
        else:
            record = run_check(args, env)
        report['checks'].append(record)
        print(record['status'].upper(), args[0], flush=True)

    passed = sum(check['status'] == 'passed' for check in report['checks'])
    excluded = sum(check['status'] == 'not_applicable' for check in report['checks'])
    failures = len(report['checks']) - passed - excluded
    report.update(
        finished_at_utc=timestamp(), status='failed' if failures else 'passed',
        passed=passed, failed=failures, not_applicable=excluded,
    )
    write_atomic(report_path, json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'{passed} passed, {failures} failed, {excluded} not applicable. Report: {report_path}')
    return int(failures != 0)


if __name__ == '__main__':
    sys.exit(main())
