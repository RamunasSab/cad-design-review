/* This calculator intentionally stays in English in all website languages. */
(()=>{'use strict';
const form=document.querySelector('#fit-form');if(!form)return;
const el=id=>document.querySelector('#fit-'+id),catalogue=window.CAD_FIT_APPLICATIONS.applications,engine=window.CADISO286;
const basis=()=>form.querySelector('[name="basis"]:checked').value;
const types={clearance:'Clearance fit',transition:'Transition fit',interference:'Interference fit'};
const format=n=>new Intl.NumberFormat('en',{useGrouping:false,minimumFractionDigits:3,maximumFractionDigits:6}).format(Math.abs(n)<1e-10?0:n);
const signed=n=>n>0?'+'+format(n):n<0?format(n):'0';
function available(){const b=basis(),size=el(b).value,type=el('type').value;if(!type||!size.trim())return[];return catalogue.filter(a=>a.basis==='both'||a.basis===b).filter(a=>{try{return engine.calculate(a.code,size).type===type}catch{return false}});}
function rebuild(){const select=el('application'),previous=select.value,rows=available();select.replaceChildren(new Option('Choose an application',''));for(const a of rows)select.add(new Option(a.name+' — '+a.application+' · '+a.code,a.id));select.disabled=!rows.length;if(rows.some(a=>a.id===previous))select.value=previous;}
function render(){const b=basis(),size=el(b).value;el('hole').disabled=b!=='hole';el('shaft').disabled=b!=='shaft';el('result-content').hidden=true;el('application-note').hidden=true;el('result').dataset.state='incomplete';el('status').hidden=false;el('status').textContent='Enter a diameter, then choose a fit type and application.';
 if(!size.trim())return;try{engine.deviations('H7',size,true)}catch{el('status').textContent='Enter a finite diameter: 0 < D ≤ 500 mm, up to 6 decimal places.';el('result').dataset.state='invalid';return;}
 if(!el('type').value)return;if(el('application').disabled){el('status').textContent='No supported applications for this system, type and diameter.';return;}
 const app=catalogue.find(a=>a.id===el('application').value);if(!app)return;
 let r;try{r=engine.calculate(app.code,size)}catch{el('status').textContent='This fit is not supported at the entered diameter.';el('result').dataset.state='invalid';return;}
 el('application-note').hidden=false;el('application-note').textContent=app.name+' · '+app.application;el('result').dataset.state='ready';el('status').hidden=true;el('result-content').hidden=false;el('designation').textContent='Ø'+format(r.nominal_mm)+' '+r.designation;el('badge').textContent=types[r.type];el('badge').dataset.type=r.type;
 const codes=r.designation.split('/');for(const [feature,code] of [['hole',codes[0]],['shaft',codes[1]]]){const dev=r[feature+'_deviations_um'],limits=r[feature+'_limits_mm'];el(feature+'-class').textContent=(feature==='hole'?'Hole ':'Shaft ')+code;el(feature+'-upper').textContent=signed(dev[1]/1000);el(feature+'-lower').textContent=signed(dev[0]/1000);el(feature+'-maximum').textContent=format(limits[1]);el(feature+'-minimum').textContent=format(limits[0]);el(feature+'-tolerance').textContent=format((dev[1]-dev[0])/1000);}
 const [lo,hi]=r.signed_difference_mm;const labels=r.type==='clearance'?['MAX CLEARANCE','MIN CLEARANCE']:r.type==='interference'?['MAX INTERFERENCE','MIN INTERFERENCE']:['MAX CLEARANCE','MAX INTERFERENCE'];const values=r.type==='clearance'?[hi,lo]:r.type==='interference'?[-lo,-hi]:[hi,-lo];for(let i=0;i<2;i++){el('metric-label-'+(i+1)).textContent=labels[i];el('metric-value-'+(i+1)).textContent=format(values[i]);}el('mean').textContent=signed((lo+hi)/2);
}
form.addEventListener('input',e=>{if(e.target!==el('application'))rebuild();render()});form.addEventListener('change',e=>{if(e.target!==el('application'))rebuild();render()});form.addEventListener('reset',()=>setTimeout(()=>{rebuild();render()},0));rebuild();render();
})();
