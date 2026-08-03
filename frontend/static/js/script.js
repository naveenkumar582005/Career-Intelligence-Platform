// =======================================================
// File: frontend/static/js/script.js
// Career Intelligence Platform Frontend Client Logic
// Communicates with Backend API on http://localhost:5000
// =======================================================

const BACKEND_API = "http://localhost:5000";

document.addEventListener("DOMContentLoaded", () => {
    console.log("Career Intelligence Platform Frontend Client Loaded (Connecting to " + BACKEND_API + ")");

    initializeTooltips();
    initializeAnimations();
    initializeFileUpload();
    initializeSkillTags();
    initializeBackToTop();

    // If on dashboard page, render dashboard UI
    if (document.getElementById("dashboardContent")) {
        renderDashboardUI();
    }
});

// =======================================================
// API Integration & Form Submission
// =======================================================

async function handleAssessmentSubmit(event) {
    event.preventDefault();

    const form = event.target;

    // Validate CGPA
    const cgpaInput = form.querySelector("[name='cgpa']");
    if (cgpaInput && (parseFloat(cgpaInput.value) < 0 || parseFloat(cgpaInput.value) > 10)) {
        alert("CGPA must be between 0.00 and 10.00");
        return;
    }

    const submitBtn = document.getElementById("submitBtn");
    const loadingStatus = document.getElementById("loadingStatus");

    if (submitBtn) submitBtn.disabled = true;
    if (loadingStatus) loadingStatus.style.display = "block";

    const formData = new FormData(form);

    try {
        const response = await fetch(`${BACKEND_API}/api/analyze`, {
            method: "POST",
            body: formData,
        });

        const result = await response.json();

        if (response.ok && result.status === "success") {
            // Save analysis context in localStorage
            localStorage.setItem("analysis_results", JSON.stringify(result.data));
            // Navigate to Dashboard on Port 3000
            window.location.href = "/dashboard";
        } else {
            alert("Error: " + (result.message || "Failed to process career analysis."));
        }
    } catch (error) {
        console.error("API Connection Error:", error);
        alert("Failed to connect to Backend Server on http://localhost:5000. Please ensure the backend is running.");
    } finally {
        if (submitBtn) submitBtn.disabled = false;
        if (loadingStatus) loadingStatus.style.display = "none";
    }
}

// =======================================================
// Dashboard UI Renderer (From localStorage)
// =======================================================

function renderDashboardUI() {
    const rawData = localStorage.getItem("analysis_results");
    const noDataAlert = document.getElementById("noDataAlert");
    const dashboardContent = document.getElementById("dashboardContent");

    if (!rawData) {
        if (noDataAlert) noDataAlert.style.display = "block";
        if (dashboardContent) dashboardContent.style.display = "none";
        return;
    }

    if (noDataAlert) noDataAlert.style.display = "none";
    if (dashboardContent) dashboardContent.style.display = "block";

    try {
        const data = JSON.parse(rawData);

        // Header & Timestamp
        const timeEl = document.getElementById("generatedAtTime");
        if (timeEl) timeEl.innerText = "Generated: " + (data.generated_at || "");

        // Summary KPI Cards
        document.getElementById("kpiPlacementProb").innerText = `${data.placement_probability}%`;
        document.getElementById("kpiResumeScore").innerText = data.resume_score;
        document.getElementById("kpiTechStrength").innerText = data.technical_strength;
        document.getElementById("kpiCareerReadiness").innerText = data.career_readiness;

        // Placement Prediction
        document.getElementById("placementResultText").innerText = data.placement_result;
        const probBar = document.getElementById("placementProbBar");
        probBar.style.width = `${data.placement_probability}%`;
        probBar.innerText = `${data.placement_probability}%`;

        // Career Readiness
        const readinessBar = document.getElementById("careerReadinessBar");
        readinessBar.style.width = `${data.career_readiness}%`;
        readinessBar.innerText = data.career_readiness;
        document.getElementById("readinessLevelHeading").innerText = data.readiness_level;
        document.getElementById("readinessMessageText").innerText = data.readiness_message;

        // Resume Intelligence Bars
        const barResume = document.getElementById("barResumeScore");
        barResume.style.width = `${data.resume_score}%`;
        barResume.innerText = data.resume_score;

        const barTech = document.getElementById("barTechStrength");
        barTech.style.width = `${data.technical_strength}%`;
        barTech.innerText = data.technical_strength;

        const barIndustry = document.getElementById("barIndustryReadiness");
        barIndustry.style.width = `${data.industry_readiness}%`;
        barIndustry.innerText = data.industry_readiness;

        // Charts from Backend
        if (data.charts) {
            document.getElementById("imgShapSummary").src = data.charts.shap_summary;
            document.getElementById("imgResumeChart").src = data.charts.resume_chart;
            document.getElementById("imgPlacementChart").src = data.charts.placement_chart;
        }

        // Recommended Jobs Table
        const jobsTbody = document.getElementById("recommendedJobsTbody");
        jobsTbody.innerHTML = "";
        (data.recommended_jobs || []).forEach((job, index) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${index + 1}</td>
                <td class="fw-semibold">${job.job_title}</td>
                <td>
                    <div class="progress" style="height: 20px;">
                        <div class="progress-bar bg-success fs-7" style="width: ${job.match_score}%;">
                            ${parseFloat(job.match_score).toFixed(2)}%
                        </div>
                    </div>
                </td>
            `;
            jobsTbody.appendChild(tr);
        });

        // Missing Skills List
        const missingUl = document.getElementById("missingSkillsUl");
        missingUl.innerHTML = "";
        if (data.missing_skills && data.missing_skills.length > 0) {
            data.missing_skills.forEach(skill => {
                const li = document.createElement("li");
                li.className = "list-group-item d-flex align-items-center";
                li.innerHTML = `<i class="bi bi-x-circle-fill text-danger me-2"></i> ${skill}`;
                missingUl.appendChild(li);
            });
        } else {
            missingUl.innerHTML = `<li class="list-group-item alert alert-success mb-0">No Skill Gap Found</li>`;
        }

        // Recommended Certifications List
        const certUl = document.getElementById("certificationsUl");
        certUl.innerHTML = "";
        if (data.certifications && data.certifications.length > 0) {
            data.certifications.forEach(cert => {
                const li = document.createElement("li");
                li.className = "list-group-item d-flex align-items-center";
                li.innerHTML = `<i class="bi bi-patch-check-fill text-success me-2"></i> ${cert}`;
                certUl.appendChild(li);
            });
        } else {
            certUl.innerHTML = `<li class="list-group-item text-muted">No specific certifications required.</li>`;
        }

        // Roadmap Table
        const roadmapTbody = document.getElementById("roadmapTbody");
        roadmapTbody.innerHTML = "";
        (data.roadmap || []).forEach((step, index) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><span class="badge bg-primary rounded-circle p-2">${index + 1}</span></td>
                <td class="fw-bold text-dark">${step.skill}</td>
                <td><span class="badge bg-secondary">${step.duration || 'Self Paced'}</span></td>
                <td>${step.task}</td>
            `;
            roadmapTbody.appendChild(tr);
        });

    } catch (e) {
        console.error("Failed to render dashboard UI:", e);
    }
}

// =======================================================
// Report Download via Backend API
// =======================================================

async function handleDownloadReport() {
    const rawData = localStorage.getItem("analysis_results");
    if (!rawData) {
        alert("No analysis report found. Please complete the career assessment first.");
        return;
    }

    try {
        const data = JSON.parse(rawData);
        const response = await fetch(`${BACKEND_API}/api/download-report`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (!response.ok) throw new Error("Failed to generate report file.");

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "career_report.txt";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    } catch (err) {
        console.error("Report download error:", err);
        alert("Could not download report file. Make sure the backend server on http://localhost:5000 is online.");
    }
}

// =======================================================
// Helper Utilities & UI Animations
// =======================================================

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(el => new bootstrap.Tooltip(el));
}

function initializeAnimations() {
    const cards = document.querySelectorAll(".card");
    cards.forEach((card, index) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(15px)";
        setTimeout(() => {
            card.style.transition = "0.5s ease-out";
            card.style.opacity = "1";
            card.style.transform = "translateY(0px)";
        }, index * 100);
    });
}

function initializeFileUpload() {
    const fileInput = document.querySelector("#resume");
    if (!fileInput) return;

    fileInput.addEventListener("change", function () {
        const file = this.files[0];
        if (!file) return;

        if (file.type !== "application/pdf") {
            alert("Only PDF files are allowed.");
            this.value = "";
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            alert("Maximum file size is 10 MB.");
            this.value = "";
        }
    });
}

function initializeSkillTags() {
    const textarea = document.querySelector("#skills");
    const container = document.querySelector("#skillPreview");
    if (!textarea || !container) return;

    textarea.addEventListener("keyup", () => {
        container.innerHTML = "";
        const skills = textarea.value.split(",");
        skills.forEach(skill => {
            skill = skill.trim();
            if (skill.length === 0) return;
            const badge = document.createElement("span");
            badge.className = "badge bg-primary m-1 p-2";
            badge.innerHTML = skill;
            container.appendChild(badge);
        });
    });
}

function initializeBackToTop() {
    const btn = document.getElementById("topBtn");
    if (!btn) return;

    window.onscroll = function () {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
            btn.style.display = "block";
        } else {
            btn.style.display = "none";
        }
    };
}

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}