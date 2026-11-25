const http = require('http');
const fs = require('fs');
const path = require('path');

const PUBLIC = path.join(__dirname, 'public');
const PORT = process.env.PORT || 8080;
const SITE_ORIGIN = 'https://vintage-press-cafe-demo.up.railway.app';
const SITE = 'Vintage Press Café';
const LANE_INBOX = 'jarvis+websites@onsmalltalk.com';

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
};

function serve(res, code, body, type) {
  res.writeHead(code, { 'Content-Type': type, 'X-Robots-Tag': 'noindex, nofollow' });
  res.end(body);
}

function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function readBody(req, cb) {
  let data = '';
  let n = 0;
  req.on('data', (chunk) => {
    n += chunk.length;
    if (n > 64 * 1024) { req.destroy(); return; }
    data += chunk;
  });
  req.on('end', () => cb(null, data));
  req.on('error', (e) => cb(e, ''));
}

const PIXEL = fs.readFileSync(path.join(PUBLIC, 'pixel.gif'));

const server = http.createServer((req, res) => {
  let p;
  try { p = decodeURIComponent((req.url || '/').split('?')[0]); } catch (e) { return serve(res, 400, 'bad request', 'text/plain'); }

  if (p === '/healthz') return serve(res, 200, 'ok', 'text/plain');

  if (p === '/open' && (req.method === 'GET' || req.method === 'HEAD')) {
    const q = new URLSearchParams((req.url || '').split('?')[1] || '');
    console.log('OPEN ' + SITE + ' ' + JSON.stringify({ t: (q.get('t') || '').slice(0, 120), ua: (req.headers['user-agent'] || '').slice(0, 60), ts: new Date().toISOString() }));
    res.writeHead(200, {
      'Content-Type': 'image/gif',
      'Cache-Control': 'no-store, no-cache, must-revalidate',
      'X-Robots-Tag': 'noindex, nofollow',
    });
    return res.end(PIXEL);
  }

  if ((req.url || '').indexOf('utm_') !== -1) {
    const q = new URLSearchParams((req.url || '').split('?')[1] || '');
    console.log('CLICK ' + SITE + ' ' + JSON.stringify({ c: (q.get('utm_content') || '').slice(0, 120), path: p.slice(0, 100), ua: (req.headers['user-agent'] || '').slice(0, 60), ts: new Date().toISOString() }));
  }

  if (p === '/contact' && req.method === 'POST') {
    readBody(req, (err, body) => {
      if (err) return serve(res, 400, 'bad request', 'text/plain');
      const form = new URLSearchParams(body);
      const name = (form.get('name') || '').trim().slice(0, 120);
      const phone = (form.get('phone') || '').trim().slice(0, 60);
      const email = (form.get('email') || '').trim().slice(0, 120);
      const msg = (form.get('message') || '').trim().slice(0, 4000);
      if (!name && !msg) {
        return serve(res, 400, '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Missing details</title><meta name="robots" content="noindex"></head><body><h1>We need a little more</h1><p>Add your name and a message and try again.</p><p><a href="/contact">Back to the form</a></p></body></html>', 'text/html; charset=utf-8');
      }
      const key = process.env.BREVO_API_KEY;
      const subject = `${SITE} site message: ${name}${phone ? ' — ' + phone : ''}`;
      const text = `New message from the Vintage Press Café site:\n\nName: ${name}\nPhone: ${phone || '-'}\nEmail: ${email || '-'}\n\n${msg || '(no message body)'}\n`;
      const html = `<h2>New message from the Vintage Press Café site</h2><p><b>Name:</b> ${escapeHtml(name)}<br><b>Phone:</b> ${escapeHtml(phone || '-')}<br><b>Email:</b> ${escapeHtml(email || '-')}</p><p>${escapeHtml(msg || '(no message body)').replace(/\n/g, '<br>')}</p>`;
      const deliver = () => {
        console.log('CONTACT ' + SITE + ' ' + JSON.stringify({ name, phone, email, message: msg.slice(0, 200), t: new Date().toISOString() }));
        console.log('MAILSENT ' + subject);
        res.writeHead(303, { Location: '/thanks' });
        res.end();
      };
      const fail = (err2) => {
        console.error('MAILERR ' + err2);
        res.writeHead(502, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Try again</title><meta name="robots" content="noindex"></head><body><h1>We could not send that right now</h1><p>Please try again in a moment, or email hello@vintagepresscafe.com.</p><p><a href="/contact">Back to the form</a></p></body></html>');
      };
      if (!key) return fail('BREVO_API_KEY not set');
      fetch('https://api.brevo.com/v3/smtp/email', {
        method: 'POST',
        headers: { 'api-key': key, 'content-type': 'application/json', 'accept': 'application/json' },
        body: JSON.stringify({
          sender: { name: SITE + ' site', email: LANE_INBOX },
          to: [{ email: LANE_INBOX }],
          replyTo: /^[^\s@]+@[^@\s]+\.[^@\s]{2,}$/.test(email) ? { email, name } : undefined,
          subject,
          textContent: text,
          htmlContent: html,
        }),
      }).then(r => {
        if (r.ok) { deliver(); }
        else { r.text().then(t => fail('brevo ' + r.status + ' ' + t.slice(0, 200))); }
      }).catch(e => fail(e && e.message ? e.message : String(e)));
    });
    return;
  }

  if (req.method !== 'GET' && req.method !== 'HEAD') return serve(res, 405, 'method not allowed', 'text/plain');

  let file = p === '/' ? '/index.html' : p;
  if (!/\.[a-z0-9]+$/i.test(file)) file += '.html';
  let code = 200, target;
  try {
    target = path.join(PUBLIC, path.normalize(file));
    if (!target.startsWith(PUBLIC)) throw new Error('esc');
    fs.statSync(target);
  } catch (e) {
    target = path.join(PUBLIC, '404.html');
    code = 404;
  }
  const ext = path.extname(target).toLowerCase();
  fs.readFile(target, (err, data) => {
    if (err) return serve(res, 500, 'read error', 'text/plain');
    serve(res, code, data, MIME[ext] || 'application/octet-stream');
  });
});

server.listen(PORT, () => console.log('listening on ' + PORT));
