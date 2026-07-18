// Kopiert die Web-App-Assets (eine Ebene hoeher) in desktop/www, damit
// electron-packager sie mit verpackt - der Packager nimmt nur den Inhalt
// von "desktop/" mit, nicht die Elternebene.
const fs = require('fs');
const path = require('path');

const src = path.join(__dirname, '..');
const dest = path.join(__dirname, 'www');

fs.rmSync(dest, { recursive: true, force: true });
fs.mkdirSync(dest, { recursive: true });

for (const name of ['index.html', 'manifest.webmanifest', 'service-worker.js']) {
  fs.copyFileSync(path.join(src, name), path.join(dest, name));
}
fs.cpSync(path.join(src, 'icons'), path.join(dest, 'icons'), { recursive: true });

console.log('Assets synchronisiert nach desktop/www');
