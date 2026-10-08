export default function SkillCard({ skill, onEdit, onDelete }) {
  const downloadBadge = () => {
    const c = document.createElement("canvas"); c.width = 800; c.height = 800;
    const x = c.getContext("2d");
    x.fillStyle = "#fff"; x.fillRect(0, 0, c.width, c.height);
    x.fillStyle = "#111827"; x.beginPath(); x.arc(400, 380, 260, 0, Math.PI * 2); x.fill();
    x.fillStyle = "#E8D5A3"; x.font = "900 48px Inter"; x.textAlign = "center";
    x.fillText(skill.skill_name, 400, 380);
    x.fillStyle = "#C9A86A"; x.font = "700 24px Inter"; x.fillText(skill.skill_level, 400, 430);
    x.fillStyle = "#fff"; x.font = "700 18px Inter"; x.fillText("Verified by SkillBridge", 400, 700);
    const a = document.createElement("a"); a.download = `${skill.skill_name}_Badge.png`; a.href = c.toDataURL(); a.click();
  };

  return (
    <div style={{ background: "#fff", border: "1px solid #ece6d8", borderRadius: 14, overflow: "hidden", boxShadow: "0 4px 14px rgba(0,0,0,.06)" }}>
      <div style={{ height: 4, background: "linear-gradient(90deg,#C9A86A,#E8D5A3)" }} />
      <div style={{ padding: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div>
            <div style={{ fontWeight: 900, fontSize: 18 }}>{skill.skill_name}</div>
            <div style={{ display: "inline-block", marginTop: 6, background: skill.skill_level === "Expert"? "linear-gradient(90deg,#C9A86A,#E8D5A3)" : "#f5f1e8", color: skill.skill_level === "Expert"? "#fff" : "#57534e", padding: "4px 10px", borderRadius: 999, fontSize: 11, fontWeight: 800 }}>{skill.skill_level}</div>
          </div>
          <span style={{ background: "linear-gradient(90deg,#C9A86A,#E8D5A3)", color: "#fff", padding: "5px 10px", borderRadius: 999, fontSize: 11, fontWeight: 800 }}>✔ Verified</span>
        </div>

        <div style={{ marginTop: 14 }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, fontWeight: 600, marginBottom: 6 }}><span>Proficiency</span><span style={{ fontWeight: 900 }}>{skill.proficiency || 80}%</span></div>
          <div style={{ height: 6, background: "#f5f1e8", borderRadius: 999, overflow: "hidden" }}>
            <div style={{ width: `${skill.proficiency || 80}%`, height: "100%", background: "linear-gradient(90deg,#C9A86A,#8B7355)", borderRadius: 999 }} />
          </div>
          <div style={{ fontSize: 12, color: "#78716c", marginTop: 8 }}>Issued: {skill.issued || "Oct 2024"} • {skill.assessments || 12} assessments completed</div>
        </div>

        <div style={{ display: "flex", gap: 8, marginTop: 14 }}>
          <button onClick={() => onEdit(skill)} style={{ flex: 1, background: "#fff", border: "1px solid #111827", padding: 10, borderRadius: 10, fontWeight: 800, fontSize: 12, cursor: "pointer" }}>View Details →</button>
          <button onClick={downloadBadge} style={{ flex: 1, background: "#111827", color: "#fff", border: "none", padding: 10, borderRadius: 10, fontWeight: 800, fontSize: 12, cursor: "pointer" }}>⬇ Download Badge</button>
        </div>
        <button onClick={() => onDelete(skill.id)} style={{ marginTop: 8, width: "100%", border: "none", background: "transparent", color: "#ef4444", fontSize: 11, fontWeight: 700, cursor: "pointer" }}>Delete</button>
      </div>
    </div>
  );
}