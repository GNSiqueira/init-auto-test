const baseURL = `${window.location.protocol}//${window.location.host}`;

export async function request(url, method, data = null) {
    try {
        const options = {
            method: method,
            headers: { 'Content-Type': 'application/json' }
        };

        if (method !== 'GET' && data) {
            options.body = JSON.stringify(data);
        }  

        console.log("Entrou request");
        console.log(url);

        const response = await fetch(url, options);

        console.log(response);

        if (!response.ok) {
            console.error(`HTTP error! status: ${response.status}`);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.text();

    } catch (error) {
        console.error('Fetch Error:', error);
        throw error;
    }
}

export async function requestJson(url, method, data = null) {
    try {
        const options = {
            method: method,
            headers: { 'Content-Type': 'application/json' }
        };

        if (method !== 'GET' && data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();

    } catch (error) {
        console.error('Fetch Error:', error);
        throw error;
    }
}