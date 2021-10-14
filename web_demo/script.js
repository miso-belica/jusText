function show_advanced() {
    advanced_options = document.getElementById("advanced_options");
    advanced_options.style.display = "block";
    show_advanced_link = document.getElementById("show_advanced_link");
    show_advanced_link.style.display = "none";
    hide_advanced_link = document.getElementById("hide_advanced_link");
    hide_advanced_link.style.display = "";
}

function hide_advanced() {
    advanced_options = document.getElementById("advanced_options");
    advanced_options.style.display = "none";
    show_advanced_link = document.getElementById("show_advanced_link");
    show_advanced_link.style.display = "";
    hide_advanced_link = document.getElementById("hide_advanced_link");
    hide_advanced_link.style.display = "none";
}

function hide_boilerplate() {
    paragraphs = document.getElementsByTagName("p");
    for (var i=0; i<paragraphs.length; i++) {
        var paragraph = paragraphs[i];
        if (paragraph.className == "bad") {
            paragraph.style.display = "none";
        }
    }
    hide_boilerplate_link = document.getElementById("hide_boilerplate_link");
    hide_boilerplate_link.style.display = "none";
    show_boilerplate_link = document.getElementById("show_boilerplate_link");
    show_boilerplate_link.style.display = "";
}

function show_boilerplate() {
    paragraphs = document.getElementsByTagName("p");
    for (var i=0; i<paragraphs.length; i++) {
        var paragraph = paragraphs[i];
        if (paragraph.className == "bad") {
            paragraph.style.display = "";
        }
    }
    show_boilerplate_link = document.getElementById("show_boilerplate_link");
    show_boilerplate_link.style.display = "none";
    hide_boilerplate_link = document.getElementById("hide_boilerplate_link");
    hide_boilerplate_link.style.display = "";
}

function show_paragraph_details(paragraph, pdid) {
    paragraph_details = document.getElementById(pdid);
    paragraph_details.style.display = "block"; 
    if (paragraph.className == "bad")
        paragraph.style.backgroundColor = "#faa";
    else
        paragraph.style.backgroundColor = "#9f9";
}

function hide_paragraph_details(paragraph, pdid) {
    paragraph_details = document.getElementById(pdid);
    paragraph_details.style.display = "none"; 
    if (paragraph.className == "bad")
        paragraph.style.backgroundColor = "#fdd";
    else
        paragraph.style.backgroundColor = "#cfc";
}
