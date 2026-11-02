const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:360,height:740}});await p.route(/googletagmanager/,r=>r.abort());
let bad=0;for(const s of process.argv.slice(2)){await p.goto('http://localhost:4399/'+s+'/');await p.waitForTimeout(400);
const w=await p.evaluate(()=>document.documentElement.scrollWidth);if(w>360){bad++;console.log('overflow',s,w);}}
console.log('checked',process.argv.length-2,'overflow',bad);await b.close();})();
