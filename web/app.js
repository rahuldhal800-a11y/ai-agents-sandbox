const $=id=>document.getElementById(id);
async function refresh(){
  try{
    const d=await (await fetch("/api/world",{cache:"no-store"})).json();
    $("status").textContent=d.alive?"ONLINE":"KILLED";
    $("status").style.color=d.alive?"#64d9a3":"#ff7777";
    $("tick").textContent="Tick "+d.tick;
    $("world").textContent=Object.keys(d.world||{}).length;
    $("tools").textContent=(d.tools||[]).length;
    $("memory").textContent=d.memory_count||0;
    $("learning").textContent=Object.keys(d.learning||{}).length;
    $("events").textContent=JSON.stringify(d.events||[],null,2);
  }catch(e){$("status").textContent="OFFLINE"}
}
$("kill").onclick=async()=>{
  if(confirm("Kill Genesis immediately?")){
    await fetch("/api/kill",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({reason:"Operator emergency stop"})});
    refresh();
  }
};
refresh();setInterval(refresh,1000);
