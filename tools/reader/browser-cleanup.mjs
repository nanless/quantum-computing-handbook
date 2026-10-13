// CLI-only cleanup after all checks and reports are complete.
// Some installed Chrome builds leave Playwright transport handles open even
// after the browser process exits. Never let those handles hang a finished CLI.
export async function closeBrowser(browser) {
  const watchdog = setTimeout(() => {
    process.stderr.write('Browser cleanup exceeded 10 seconds; saved check results are unchanged. Exiting the CLI.\n');
    process.exit(process.exitCode ?? 0);
  }, 10000);
  try { await browser.close(); }
  finally { clearTimeout(watchdog); }
}
