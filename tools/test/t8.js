const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.route(/googletagmanager/,r=>r.abort());
const errs=[];p.on('pageerror',e=>errs.push(p.url()+' '+e.message));let warn=[];
for(const s of process.argv.slice(2)){await p.goto('http://localhost:4399/'+s+'/');await p.waitForTimeout(250);
const w=await p.evaluate(()=>[...document.querySelectorAll('.calc__status .warn')].map(x=>x.textContent).join(';'));if(w)warn.push(s+': '+w);}
console.log('pages',process.argv.length-2,'warnings',warn.length,warn.slice(0,10),'errors',errs.length,errs.slice(0,5));await b.close();})();
