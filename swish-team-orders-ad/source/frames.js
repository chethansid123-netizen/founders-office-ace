// usage: node frames.js out_prefix t1 t2 ...
const { chromium } = require('playwright');
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1080,height:1920}});
  p.on('console',m=>console.log('console:',m.text())); p.on('pageerror',e=>console.log('pageerror:',e.message));
  await p.goto('file://'+__dirname+'/'+(process.env.HTML||'ad.html')); await p.evaluate(()=>window.ready);
  for(const ts of process.argv.slice(3)){const t=parseFloat(ts);await p.evaluate(t=>render(t),t);
    await p.screenshot({path:`${process.argv[2]}_${ts}.png`,clip:{x:0,y:0,width:1080,height:1920}});}
  await b.close();
})();
