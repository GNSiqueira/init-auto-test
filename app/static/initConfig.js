import { request } from "./script.js";

async function addPath(inputId) {
    try {
        const input = document.getElementById(inputId);
        const filePath = await request('/path', 'GET'); // Substitua '/path' pela sua rota Flask real
        input.value = filePath;
    } catch (error) {
        console.error("Failed to get path:", error);
    }
}

async function pathFile(inputId) {
    try {
        const input = document.getElementById(inputId);
        const filePath = await request('/path-file', 'GET'); // Substitua '/path' pela sua rota Flask real
        input.value = filePath;
    } catch (error) {
        console.error("Failed to get path:", error);
    }
}


window.pathFile = pathFile;
window.addPath = addPath;