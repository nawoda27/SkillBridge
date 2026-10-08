import { useState, useEffect } from "react";
import jsPDF from "jspdf";

export default function CertificateCard({ certificate, onDelete }){
  const [showView,setShowView]=useState(false);

  const fmt = (d)=>{ if(!d) return ""; const dt=new Date(d); return isNaN(dt)? d : dt.toLocaleDateString("en-GB",{day:"2-digit",month:"short",year:"numeric"}); };

  const downloadPDF = ()=>{
    const doc = new jsPDF({ orientation:"landscape", unit:"pt", format:"a4" });
    const W = doc.internal.pageSize.getWidth();
    const H = doc.internal.pageSize.getHeight();

    // Gold top border
    doc.setFillColor(201,168,106);
    doc.rect(0,0,W,14,'F');
    doc.setFillColor(232,213,163);
    doc.rect(0,14,W,6,'F');

    // Outer border
    doc.setDrawColor(236,230,216);
    doc.setLineWidth(1.5);
    doc.rect(30,30,W-60,H-60);

    // Logo
    doc.setFont("helvetica","bold");
    doc.setFontSize(38);
    doc.setTextColor(17,24,39);
    doc.text("SkillBridge", W/2, 110, { align:"center" });

    doc.setFontSize(12);
    doc.setTextColor(100,116,139);
    doc.setFont("helvetica","bold");
    doc.text("CERTIFICATE OF ACHIEVEMENT", W/2, 135, { align:"center" });

    // Medal icon
    doc.setFontSize(44);
    doc.text("🏅", W/2, 180, { align:"center" });

    // Certificate name
    doc.setFontSize(28);
    doc.setTextColor(17,24,39);
    doc.setFont("helvetica","bold");
    doc.text(certificate.certificate_name || "Certificate", W/2, 230, { align:"center", maxWidth: W-120 });

    // Credential
    doc.setFontSize(14);
    doc.setTextColor(99,102,241);
    doc.text(`Credential ID: ${certificate.credential_id || "SB-XXXX"}`, W/2, 265, { align:"center" });

    // Issue date
    doc.setFontSize(13);
    doc.setTextColor(71,85,105);
    doc.setFont("helvetica","normal");
    doc.text(`Completed on ${fmt(certificate.issue_date)} • Issued by ${certificate.issuer || "SkillBridge"}`, W/2, 290, { align:"center" });

    // Skills
    if(certificate.skills?.length){
      doc.setFontSize(11);
      doc.setTextColor(120,113,108);
      doc.text(`Skills: ${certificate.skills.join(", ")}`, W/2, 315, { align:"center" });
    }

    // Verified badge
    doc.setFillColor(236,253,245);
    doc.setDrawColor(167,243,208);
    doc.roundedRect(W/2-90, 340, 180, 32, 8,8,'FD');
    doc.setFontSize(11);
    doc.setTextColor(4,120,87);
    doc.setFont("helvetica","bold");
    doc.text("✓ VERIFIED ON-CHAIN", W/2, 360, { align:"center" });

    // Footer
    doc.setFontSize(10);
    doc.setTextColor(148,163,184);
    doc.setFont("helvetica","normal");
    doc.text("This certificate is verified on-chain and shareable to LinkedIn, employers and portfolio", W/2, H-45, { align:"center" });

    doc.save(`${(certificate.certificate_name||"certificate").replace(/\s+/g,"_")}.pdf`);
  };

  useEffect(()=>{
    const h=(e)=>{ if(e.detail?.id===certificate.id || e.detail?.certificate_name===certificate.certificate_name) downloadPDF(); };
    window.addEventListener("sb_download_one",h);
    return ()=>window.removeEventListener("sb_download_one",h);
  },[certificate]);

  return (
    <>
      <div style={{ background:"#fff", border:"1px solid #ece6d8", borderRadius:14, overflow:"hidden", boxShadow:"0 4px 14px rgba(0,0,0,.06)" }}>
        <div style={{ height:14, background:"linear-gradient(90deg,#c9a86a,#e8d5a3,#c9a86a)" }} />
        <div style={{ padding:14 }}>
          <div style={{ display:"flex", gap:10, alignItems:"center", marginBottom:10 }}>
            <div style={{ width:32, height:40, background:"linear-gradient(180deg,#e8d5a3,#c9a86a)", clipPath:"polygon(0 0,100% 0,100% 75%,50% 100%,0 75%)", display:"flex", alignItems:"center", justifyContent:"center", color:"#fff", fontSize:16 }}>🏅</div>
            <span style={{ background:"#f5f1e8", border:"1px solid #ece6d8", padding:"4px 10px", borderRadius:999, fontSize:11, fontWeight:700 }}>✔ Verified</span>
          </div>

          <div style={{ fontWeight:800, fontSize:16, lineHeight:1.3, minHeight:44 }}>{certificate.certificate_name}</div>
          <div style={{ marginTop:10, display:"inline-flex", alignItems:"center", gap:6, background:"#f9f6f0", border:"1px solid #f0e6d0", borderRadius:8, padding:"6px 10px", fontSize:12, fontWeight:600 }}>📅 Completed {fmt(certificate.issue_date)}</div>
          <div style={{ display:"flex", gap:6, flexWrap:"wrap", marginTop:12 }}>
            {certificate.skills?.map((s,i)=><span key={i} style={{ background:"#fdf2d5", border:"1px solid #f0d9a0", padding:"5px 10px", borderRadius:999, fontSize:11, fontWeight:700 }}>{s}</span>)}
          </div>
          <div style={{ marginTop:14, fontSize:11, color:"#78716c" }}>Issued by SkillBridge • Credential ID: {certificate.credential_id}</div>

          <div style={{ display:"flex", gap:8, marginTop:12 }}>
            <button onClick={()=>setShowView(true)} style={{ flex:1, background:"#111827", color:"#fff", border:"none", padding:"10px", borderRadius:8, fontWeight:800, fontSize:12, cursor:"pointer" }}>View Certificate</button>
            <button onClick={downloadPDF} style={{ flex:1, background:"#fff", border:"1px solid #111827", padding:"10px", borderRadius:8, fontWeight:800, fontSize:12, cursor:"pointer" }}>⬇ Download PDF</button>
          </div>
          <button onClick={()=>onDelete(certificate.id)} style={{ marginTop:8, width:"100%", border:"none", background:"transparent", color:"#ef4444", fontSize:11, fontWeight:700, cursor:"pointer" }}>Delete</button>
        </div>
      </div>

      {showView && (
        <div style={{ position:"fixed", inset:0, background:"rgba(0,0,0,.5)", backdropFilter:"blur(6px)", display:"flex", alignItems:"center", justifyContent:"center", zIndex:100 }} onClick={()=>setShowView(false)}>
          <div onClick={e=>e.stopPropagation()} style={{ width:680, background:"#fff", borderRadius:18, overflow:"hidden" }}>
            <div style={{ height:10, background:"linear-gradient(90deg,#c9a86a,#e8d5a3,#c9a86a)" }} />
            <div style={{ padding:28, textAlign:"center" }}>
              <div style={{ fontSize:40 }}>🎓</div>
              <div style={{ fontSize:11, fontWeight:800, color:"#94a3b8", letterSpacing:.8, marginTop:8 }}>CERTIFICATE OF ACHIEVEMENT</div>
              <h2 style={{ margin:"10px 0", fontWeight:900, fontSize:26 }}>{certificate.certificate_name}</h2>
              <div style={{ color:"#6366f1", fontWeight:700 }}>{certificate.issuer} • {certificate.credential_id}</div>
              <div style={{ marginTop:20, background:"#ecfdf5", border:"1px solid #a7f3d0", padding:12, borderRadius:10, color:"#047857", fontWeight:700 }}>✓ Verified on-chain</div>
              <div style={{ display:"flex", gap:10, marginTop:20 }}><button onClick={downloadPDF} style={{ flex:1, background:"#111827", color:"#fff", border:"none", padding:12, borderRadius:999, fontWeight:800 }}>⬇ Download PDF</button><button onClick={()=>setShowView(false)} style={{ padding:"12px 18px", borderRadius:999, border:"1px solid #e7e0d2", background:"#fff" }}>Close</button></div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}