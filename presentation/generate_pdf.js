#!/usr/bin/env node
/**
 * Generate PDF from presentation HTML using Puppeteer
 * Usage: node generate_pdf.js
 */

const puppeteer = require('puppeteer-core');
const path = require('path');

(async () => {
    const htmlPath = path.resolve(__dirname, 'presentation.html');
    const outputPath = path.resolve(__dirname, 'WorkHere_Presentation.pdf');

    console.log('Launching browser...');
    const browser = await puppeteer.launch({
        headless: 'new',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--font-render-hinting=none'
        ],
        executablePath: '/usr/local/bin/google-chrome'
    });

    const page = await browser.newPage();

    // Set viewport to match slide dimensions
    await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2 });

    console.log('Loading presentation...');
    await page.goto(`file://${htmlPath}`, {
        waitUntil: 'networkidle0',
        timeout: 30000
    });

    // Wait for fonts to load
    await page.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 2000));

    console.log('Generating PDF...');
    await page.pdf({
        path: outputPath,
        width: '1280px',
        height: '720px',
        printBackground: true,
        preferCSSPageSize: true,
        margin: { top: 0, right: 0, bottom: 0, left: 0 }
    });

    await browser.close();

    const fs = require('fs');
    const stats = fs.statSync(outputPath);
    console.log(`PDF created: ${outputPath}`);
    console.log(`Size: ${(stats.size / 1024).toFixed(1)} KB`);
})().catch(err => {
    console.error('Error:', err);
    process.exit(1);
});
