const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.route(/googletagmanager/,r=>r.abort());
for(const s of process.argv.slice(2)){await p.goto('http://localhost:4399/'+s+'/');await p.waitForTimeout(800);
console.log(s,'=>',await p.evaluate(()=>[...document.querySelectorAll('.calc .field')].map(f=>(f.querySelector('label')?.textContent||'').trim().slice(0,22)+'='+([...f.querySelectorAll('input,select')].map(i=>i.value).join(' '))).join(' | ')));}
await b.close();})();
