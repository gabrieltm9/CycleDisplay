function changePage(newPage) {
    localStorage.setItem('newPage', newPage);
    console.log('Page changed to ' + newPage);
}