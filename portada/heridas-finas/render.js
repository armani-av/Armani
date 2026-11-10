const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:1000},deviceScaleFactor:+process.argv[3]||1});
await p.goto('file://'+process.argv[2]);await p.waitForSelector('body[data-ready]');await p.waitForTimeout(800);
await p.screenshot({path:process.argv[4]});await b.close()})();
