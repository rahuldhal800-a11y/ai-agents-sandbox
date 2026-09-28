const $=id=>document.getElementById(id);
function renderSimulation(s,d){const t=s.terrain||[];const g=(s.entities||[]).find(e=>e.id==="genesis");const r=new Set((s.resources||[]).filter(x=>x.amount>0).map(x=>x.x+","+x.y));$("grid").innerHTML="";for(let y=0;y<t.length;y++){for(let x=0;x<t[y].length;x++){const c=document.createElement("div");c.className="cell "+(t[y][x]||"plain");if(r.has(x+","+y))c.classList.add("resource");if(g&&g.x===x&&g.y===y){c.classList.add("genesis");c.title="Genesis";}$("grid").appendChild(c)}}if(g)$("simMeta").textContent=`Genesis • (${g.x}, ${g.y}) • ${g.status} • energy ${g.energy.toFixed(0)} • hunger ${g.hunger} • thirst ${g.thirst} • age ${g.age} • mutations ${d.mutations||0} • experiences ${d.experiences||0}`;}
function escapeHtml(v){return String(v).replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
const synth=window.speechSynthesis;
let recognition=null;
let speaking=false;

function addBubble(who,text){
  const el=document.createElement("div");
  el.className="bubble "+(who==="GENESIS"?"genesis":"user");
  el.innerHTML="<span>"+who+"</span><p></p>";
  el.querySelector("p").textContent=text;
  $("conversation").appendChild(el);
  $("conversation").scrollTop=$("conversation").scrollHeight;
}
function speak(text){
  if(!synth||!text)return;
  synth.cancel();
  const u=new SpeechSynthesisUtterance(text);
  u.rate=.98;u.pitch=1;
  u.onstart=()=>{$("voiceState").textContent="GENESIS SPEAKING";speaking=true};
  u.onend=()=>{$("voiceState").textContent="VOICE READY";speaking=false};
  synth.speak(u);
}
async function talk(message){
  const text=message.trim();
  if(!text)return;
  addBubble("YOU",text);
  $("message").value="";
  $("activityState").textContent="GENESIS THINKING";
  try{
    const res=await fetch("/api/talk",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text})});
    const data=await res.json();
    const reply=data.reply||data.error||"No response.";
    addBubble("GENESIS",reply);
    speak(reply);
  }catch(e){addBubble("GENESIS","I cannot reach my world server right now.");}
  $("activityState").textContent="WORLD ACTIVE";
  refresh();
}
function setupVoice(){
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){$("voiceState").textContent="VOICE UNSUPPORTED";return;}
  recognition=new SR();recognition.lang="en-IN";recognition.interimResults=false;recognition.continuous=false;
  recognition.onstart=()=>{$("mic").classList.add("recording");$("voiceState").textContent="LISTENING…"};
  recognition.onresult=e=>{const text=e.results[0][0].transcript;$("message").value=text;talk(text)};
  recognition.onerror=()=>{$("mic").classList.remove("recording");$("voiceState").textContent="VOICE READY"};
  recognition.onend=()=>{$("mic").classList.remove("recording");if(!speaking)$("voiceState").textContent="VOICE READY"};
  $("mic").onclick=()=>{try{recognition.start()}catch(e){}};
}
async function refresh(){
  try{
    const d=await (await fetch("/api/world",{cache:"no-store"})).json();
    $("status").textContent=d.alive?"ONLINE":"STOPPED";
    $("status").style.color=d.alive?"#6ff0b0":"#ff7777";
    $("tick").textContent="TICK "+d.tick;
    const s=d.world||{};
    renderSimulation(s,d);
    $("worldTime").textContent=(s.time||"00:00")+" • "+(s.cycle||"unknown").toUpperCase();
    $("entities").innerHTML=(s.entities||[]).map(e=>`<div class="entity"><b>${escapeHtml(e.name)}</b><small>${escapeHtml(e.type)} · ${escapeHtml(e.status)}</small><div class="node"><i></i></div></div>`).join("");
    $("world").textContent=Object.keys(d.world||{}).length;
    $("tools").textContent=(d.tools||[]).length;
    $("memory").textContent=d.memory_count||0;
    $("learning").textContent=Object.keys(d.learning||{}).length;
    $("events").textContent=JSON.stringify(d.events||[],null,2);
    if(!d.alive)$("activityState").textContent="GENESIS STOPPED";
  }catch(e){$("status").textContent="OFFLINE";$("activityState").textContent="WORLD OFFLINE";}
}
$("send").onclick=()=>talk($("message").value);
$("message").addEventListener("keydown",e=>{if(e.key==="Enter")talk($("message").value)});
document.querySelectorAll(".quick button").forEach(b=>b.onclick=()=>talk(b.dataset.message));
$("kill").onclick=async()=>{
  if(confirm("Stop Genesis immediately?")){
    await fetch("/api/kill",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({reason:"Operator emergency stop"})});
    refresh();
  }
};
setupVoice();refresh();setInterval(refresh,1000);
