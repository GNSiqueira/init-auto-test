import { requestJson } from "./script.js";

function alterShowModal(className, action) {
    const modal = document.querySelector(`.${className}`);
    modal.style.display = action;
}

function insertInformation(systemname) {
    const SystemName = document.getElementById('editSystemName');
    const editSystemNameOld = document.getElementById('editSystemNameOld');
    const debugSystem = document.getElementById('debugSystem');
    const debugSystemOld = document.getElementById('debugSystemOld');
    const keySelect = document.getElementById('keySelect');
    const keySystemOld = document.getElementById('keySystemOld');

    requestJson('/edit-system?systemName=' + systemname, 'GET').then(data => {
        SystemName.ariaPlaceholder = data['systemName'];

        SystemName.value = data['systemName'];
        
        keySelect.innerHTML = `<option value=""></option>`;
        
        debugSystem.innerHTML = `<option value=""></option>`;

        editSystemNameOld.value = data['systemName'];

        
        debugSystemOld.value = data['debugSystem'];
        keySystemOld.value = data['keySelect'];

        data['listKeys'].forEach(element => {
            keySelect.innerHTML += `<option value="${element}" ${data['keySelect'] === element ? 'selected' : ''}>${element}</option>`;
        });
        data['listDebugs'].forEach(element => {
            debugSystem.innerHTML += `<option value="${element}" ${data['debugSystem'] === element ? 'selected' : ''}>${element}</option>`;
        });
    })
}

function insertInformationBase() {
    const keySelect = document.getElementById('keySelectBase');
    const keySystemOld = document.getElementById('keySystemOldBase');
    const label = document.getElementById('editSystemNameBase');
    
    requestJson('/edit-system-base', 'GET').then(data => {
        console.log(data)

        label.value = data['systemName'];

        keySelect.innerHTML = `<option value=""></option>`;
        
        keySystemOld.value = data['keySelect'];

        
        data['listKeys'].forEach(element => {
            keySelect.innerHTML += `<option value="${element}" ${data['keySelect'] === element ? 'selected' : ''}>${element}</option>`;
        });
    })
}

function timeAlert() {
    const alert = document.getElementById('message');
    setTimeout(() => {
        alert.style.color = 'transparent';
    }, 10000);
}

function searchBar() {
    const searchInput = document.getElementById('search');

    const searchTerm = searchInput.value.trim();

    const searchURL = '/?search=' + encodeURIComponent(searchTerm);

    window.location.href = searchURL;
}

function searchBarDebug() {
    const searchInput = document.getElementById('search');

    const searchTerm = searchInput.value.trim();

    const searchURL = '/debug?search=' + encodeURIComponent(searchTerm);

    window.location.href = searchURL;
}

function handleEnter(event) {
    // Verifica se a tecla pressionada é o Enter (keyCode 13 ou key 'Enter')
    if (event.key === 'Enter' || event.keyCode === 13) {
        event.preventDefault(); // Impede o envio padrão do formulário se houver um
        searchBar(); // Chama sua função de busca
    }
}

window.handleEnter = handleEnter;

window.searchBarDebug = searchBarDebug;

timeAlert();

window.searchBar = searchBar;

window.insertInformationBase = insertInformationBase;

window.insertInformation = insertInformation;

window.alterShowModal = alterShowModal;
