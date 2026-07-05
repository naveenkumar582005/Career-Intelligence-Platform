// =======================================================
// File: static/js/script.js
// =======================================================

document.addEventListener("DOMContentLoaded", () => {

    console.log("Career Intelligence Platform Loaded");

    initializeTooltips();

    initializeAnimations();

    initializeCounters();

    initializeProgressBars();

    initializeFileUpload();

    initializeSkillTags();

    initializeBackToTop();

});

// =======================================================
// Bootstrap Tooltips
// =======================================================

function initializeTooltips() {

    const tooltipTriggerList = [].slice.call(

        document.querySelectorAll('[data-bs-toggle="tooltip"]')

    );

    tooltipTriggerList.map(function (tooltipTriggerEl) {

        return new bootstrap.Tooltip(tooltipTriggerEl);

    });

}

// =======================================================
// Fade Animation
// =======================================================

function initializeAnimations() {

    const cards = document.querySelectorAll(".card");

    cards.forEach((card, index) => {

        card.style.opacity = "0";

        card.style.transform = "translateY(20px)";

        setTimeout(() => {

            card.style.transition = "0.6s";

            card.style.opacity = "1";

            card.style.transform = "translateY(0px)";

        }, index * 150);

    });

}

// =======================================================
// Counter Animation
// =======================================================

function animateValue(element, start, end, duration) {

    let range = end - start;

    let current = start;

    let increment = end > start ? 1 : -1;

    let stepTime = Math.abs(Math.floor(duration / range));

    let timer = setInterval(() => {

        current += increment;

        element.innerHTML = current;

        if (current === end) {

            clearInterval(timer);

        }

    }, stepTime);

}

function initializeCounters() {

    document.querySelectorAll(".counter").forEach(counter => {

        const target = parseInt(counter.dataset.target);

        animateValue(counter, 0, target, 1200);

    });

}

// =======================================================
// Progress Bars
// =======================================================

function initializeProgressBars() {

    const bars = document.querySelectorAll(".progress-bar");

    bars.forEach(bar => {

        const width = bar.style.width;

        bar.style.width = "0%";

        setTimeout(() => {

            bar.style.transition = "1.5s";

            bar.style.width = width;

        }, 300);

    });

}

// =======================================================
// Resume Upload Validation
// =======================================================

function initializeFileUpload() {

    const fileInput = document.querySelector("#resume");

    if (!fileInput) return;

    fileInput.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) return;

        const allowed = ["application/pdf"];

        if (!allowed.includes(file.type)) {

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

// =======================================================
// Skill Tags
// =======================================================

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

            badge.className =

                "badge bg-primary m-1 p-2";

            badge.innerHTML = skill;

            container.appendChild(badge);

        });

    });

}

// =======================================================
// Dashboard Search
// =======================================================

function searchTable(inputId, tableId) {

    const input = document.getElementById(inputId);

    const filter = input.value.toUpperCase();

    const table = document.getElementById(tableId);

    const tr = table.getElementsByTagName("tr");

    for (let i = 0; i < tr.length; i++) {

        let td = tr[i].getElementsByTagName("td")[0];

        if (td) {

            let txtValue = td.textContent || td.innerText;

            if (

                txtValue.toUpperCase().indexOf(filter) > -1

            ) {

                tr[i].style.display = "";

            } else {

                tr[i].style.display = "none";

            }

        }

    }

}

// =======================================================
// Theme Toggle
// =======================================================

function toggleTheme() {

    document.body.classList.toggle("dark-mode");

}

// =======================================================
// Scroll To Top
// =======================================================

function initializeBackToTop() {

    const btn = document.getElementById("topBtn");

    if (!btn) return;

    window.onscroll = function () {

        if (

            document.body.scrollTop > 300 ||

            document.documentElement.scrollTop > 300

        ) {

            btn.style.display = "block";

        }

        else {

            btn.style.display = "none";

        }

    };

}

function topFunction() {

    document.body.scrollTop = 0;

    document.documentElement.scrollTop = 0;

}

// =======================================================
// Download Report
// =======================================================

function downloadReport() {

    window.location.href = "/download_report";

}

// =======================================================
// Success Notification
// =======================================================

function showSuccess(message) {

    alert(message);

}

// =======================================================
// Loading Spinner
// =======================================================

function showLoader() {

    const loader = document.getElementById("loader");

    if (loader)

        loader.style.display = "flex";

}

function hideLoader() {

    const loader = document.getElementById("loader");

    if (loader)

        loader.style.display = "none";

}

// =======================================================
// Form Validation
// =======================================================

function validateForm() {

    const cgpa = document.querySelector("[name='cgpa']").value;

    if (cgpa < 0 || cgpa > 10) {

        alert("CGPA must be between 0 and 10");

        return false;

    }

    return true;

}

// =======================================================
// Footer Year
// =======================================================

const year = document.getElementById("year");

if (year) {

    year.innerHTML = new Date().getFullYear();

}