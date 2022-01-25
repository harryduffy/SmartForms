window.onload = function() {

    function tableConfigure() {

        const tableConfigure = document.getElementById('table-configure-modal');
        const modalContainer = document.getElementById('table-configure-modal-container');

        const body = document.body.style.backgroundColor('black');
        if (modalContainer.style.display === 'block') {
            tableConfigure.style.display = 'none';
            modalContainer.style.display = 'none';
        } else {
            modalContainer.style.display = 'block';
            tableConfigure.style.display = 'block';
            tableConfigure.style.zIndex = 10003;
        }
    }
    
    const tableConfigureModalExit = document.getElementById('table-configure-modal-exit');
    const tableConfigureVar = document.getElementById('table-configure');
    tableConfigureVar.onclick = tableConfigure;
    tableConfigureModalExit.onclick = tableConfigure;
}