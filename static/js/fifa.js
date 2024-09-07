const sheetId = '1AYi1eyzHwZgTCOccHKLhAGVMfaCqqgiePkdRtV1DdQY';  // Replace with your Google Sheet ID
const apiKey = "AIzaSyCyuBAZndcwnqE61f0RYSgmyyzaZbxVdxg";

const base = `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values:batchGet?ranges=Sheet1&key=${apiKey}`;


function fetchData() {
    fetch(base)
        .then(response => response.json())
        .then(data => {
            const values = data.valueRanges[0].values;

            // Parse data into sections
            const headToHeadData = parseHeadToHead(values);
            const totalGoalsData = calculateTotalGoals(values);
            const recentGamesData = parseRecentGames(values);

            // Update HTML with parsed data
            updateHeadToHeadTable(headToHeadData);
            updateTotalGoalsTable(totalGoalsData);
            updateRecentGamesTable(recentGamesData);
        })
        .catch(err => console.error(err));
}

// Parsing for the head-to-head table
function parseHeadToHead(values) {
    const headToHead = [];
    for (let i = 2; i <= 6; i++) {
        // Ensure values are populated, otherwise fill with "0"
        const row = values[i].slice(11, 17).map(cell => cell || '0');  // Columns K-R (adjust based on your Google Sheet)
        headToHead.push(row);
    }
    return headToHead;
}

// Parsing for the total goals table
function calculateTotalGoals(values) {
    const totalGoals = [];
    const totalGoalsIndex = values.findIndex(row => row.includes('Total Goals'));
    const rowStart = totalGoalsIndex + 1;
    for (let i = rowStart; i < values.length; i++) {
        const player = values[i][11] || '';  // Adjust for correct columns
        const goals = values[i][12] || '0';  // Ensure 0 is shown if goals are empty
        totalGoals.push([player, goals]);
    }
    return totalGoals;
}

// Parsing for the recent games log (last 5 games)
function parseRecentGames(values) {
    const recentGames = [];
    const gameRows = values.slice(1, 6);  // Assuming first row is header, take 5 most recent
    gameRows.forEach(row => {
        const gameData = [
            row[0] || '',  // Player 1
            row[1] || '',  // Team 1
            row[2] || '0',  // Player 1 Goals
            row[3] || '',  // Player 2
            row[4] || '',  // Team 2
            row[5] || '0'   // Player 2 Goals
        ];  // Adjust indices as per your table
        recentGames.push(gameData);
    });
    return recentGames;
}

// Update head-to-head table
function updateHeadToHeadTable(data) {
    const table = document.getElementById('headToHeadTable').querySelector('tbody');
    table.innerHTML = '';  // Clear existing data
    data.forEach(row => {
        const tr = document.createElement('tr');
        row.forEach(cell => {
            const td = document.createElement('td');
            td.textContent = cell;
            tr.appendChild(td);
        });
        table.appendChild(tr);
    });
}

// Update total goals table
function updateTotalGoalsTable(data) {
    const table = document.getElementById('totalGoalsTable').querySelector('tbody');
    table.innerHTML = '';  // Clear existing data
    data.forEach(row => {
        const tr = document.createElement('tr');
        row.forEach(cell => {
            const td = document.createElement('td');
            td.textContent = cell;
            tr.appendChild(td);
        });
        table.appendChild(tr);
    });
}

// Update recent games log
function updateRecentGamesTable(data) {
    const table = document.getElementById('recentGamesTable').querySelector('tbody');
    table.innerHTML = '';  // Clear existing data
    data.forEach(row => {
        const tr = document.createElement('tr');
        row.forEach(cell => {
            const td = document.createElement('td');
            td.textContent = cell;
            tr.appendChild(td);
        });
        table.appendChild(tr);
    });
}

fetchData();