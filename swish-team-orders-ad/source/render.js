// node render.js out.mp4 [fps] [html]   env: DUR (seconds, default 15), AUDIO (wav, default soundtrack.wav)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const FFMPEG = process.env.FFMPEG;
(async()=>{
  const out=process.argv[2], fps=parseInt(process.argv[3]||'60'), html=process.argv[4]||'ad.html';
  const W=parseInt(process.env.W||'1080'), H=parseInt(process.env.H||'1920');
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:W,height:H}});
  p.on('pageerror',e=>console.log('pageerror:',e.message));
  await p.goto('file://'+__dirname+'/'+html); await p.evaluate(()=>window.ready);
  const ff=spawn(FFMPEG,['-y','-loglevel','error','-framerate',String(fps),'-f','image2pipe','-c:v','png','-i','-',
    '-i',(process.env.AUDIO||'soundtrack.wav'),'-map','0:v','-map','1:a',
    '-c:v','libx264','-preset','slow','-crf','15','-pix_fmt','yuv420p','-profile:v','high','-level','4.2',
    '-r',String(fps),'-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',out],{stdio:['pipe','inherit','inherit']});
  const total=Math.round(parseFloat(process.env.DUR||'15')*fps); const t0=Date.now();
  for(let i=0;i<total;i++){
    const t=i/fps; await p.evaluate(t=>render(t),t);
    const buf=await p.screenshot({type:'png',clip:{x:0,y:0,width:W,height:H}});
    if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));
    if(i%60===0) console.log(`frame ${i}/${total} ${((Date.now()-t0)/1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await b.close(); console.log('done',out);
})();
