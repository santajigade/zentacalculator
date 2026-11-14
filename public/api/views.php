<?php
// Page view counter for zentacalculator.com calculator pages.
// GET /api/views.php?p=/category/slug/        -> {"views": N}
// GET /api/views.php?p=/category/slug/&hit=1  -> counts one view, then returns the new total
// Counts are kept OUTSIDE public_html so deploys never wipe them.
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');

$p = isset($_GET['p']) ? (string)$_GET['p'] : '';
if (!preg_match('#^/[a-z0-9-]+/[a-z0-9-]+/$#', $p)) { http_response_code(400); echo '{"error":"bad path"}'; exit; }
$root = rtrim(isset($_SERVER['DOCUMENT_ROOT']) ? $_SERVER['DOCUMENT_ROOT'] : dirname(__DIR__), '/');
if (!is_file($root . $p . 'index.html')) { http_response_code(404); echo '{"error":"unknown page"}'; exit; }

$dir = dirname(__DIR__, 2) . '/zenta-views';
if (!is_dir($dir)) { @mkdir($dir, 0755, true); }
if (!is_dir($dir) || !is_writable($dir)) {
  $dir = __DIR__ . '/data';
  if (!is_dir($dir)) { @mkdir($dir, 0755, true); @file_put_contents($dir . '/.htaccess', "Require all denied\n"); }
}
$file = $dir . '/views.json';

$ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '';
$isBot = $ua === '' || preg_match('/bot|crawl|spider|slurp|preview|lighthouse|headless|python|curl|wget|monitor/i', $ua);
$hit = !empty($_GET['hit']) && !$isBot;

$fh = @fopen($file, 'c+');
if (!$fh) { echo '{"views":null}'; exit; }
flock($fh, $hit ? LOCK_EX : LOCK_SH);
$raw = stream_get_contents($fh);
$data = $raw ? json_decode($raw, true) : array();
if (!is_array($data)) { $data = array(); }
$n = isset($data[$p]) ? (int)$data[$p] : 0;
if ($hit) {
  $n++;
  $data[$p] = $n;
  ftruncate($fh, 0); rewind($fh);
  fwrite($fh, json_encode($data));
  fflush($fh);
}
flock($fh, LOCK_UN);
fclose($fh);
echo json_encode(array('views' => $n));
