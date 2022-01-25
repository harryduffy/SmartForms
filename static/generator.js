window.onload = function() {

    function dropdownForm() {
        const formContent = document.getElementById('form-elements');
        const formButton = document.getElementById('form-dropdown');
        if (formContent.style.display === 'block') {
            formContent.style.display = 'none';
            formButton.style.backgroundColor = '#02222f';
            formButton.style.fontWeight = 'normal';
        } else {
            formContent.style.display = 'block';
            formButton.style.backgroundColor = 'orange';
            formButton.style.fontWeight = 'bold';
        }
    }
    
    function dropdownPDF() {
        const pdfContet = document.getElementById('pdf-elements');
        const pdfButton = document.getElementById('pdf-dropdown');
        if (pdfContet.style.display === 'block') {
            pdfContet.style.display = 'none';
            pdfButton.style.backgroundColor = '#02222f';
            pdfButton.style.fontWeight = 'normal';
        } else {
            pdfContet.style.display = 'block';
            pdfButton.style.backgroundColor = 'orange';
            pdfButton.style.fontWeight = 'bold';
        }
    }

    const form_dropdown_button = document.getElementById('form-dropdown');
    form_dropdown_button.addEventListener('click', dropdownForm);

    const pdf_dropdown_button = document.getElementById('pdf-dropdown');
    pdf_dropdown_button.addEventListener('click', dropdownPDF);

    function shortQuestionModal() {
        const questionModal = document.getElementById('form-question-modal');
        const modalContainer = document.getElementById('form-question-modal-container');
        if (modalContainer.style.display === 'block') {
            questionModal.style.display = 'none';
            modalContainer.style.display = 'none';
        } else {
            modalContainer.style.display = 'block';
            questionModal.style.display = 'block';
            questionModal.style.zIndex = 10001;
        }
    }
    
    const modalExit = document.getElementById('form-question-modal-exit');
    const formQuestion = document.getElementById('short-question');
    formQuestion.onclick = shortQuestionModal;
    modalExit.onclick = shortQuestionModal;

    function longQuestionModal() {
        const questionModal = document.getElementById('long-question-modal');
        const modalContainer = document.getElementById('long-question-modal-container');
        if (modalContainer.style.display === 'block') {
            questionModal.style.display = 'none';
            modalContainer.style.display = 'none';
        } else {
            modalContainer.style.display = 'block';
            questionModal.style.display = 'block';
            questionModal.style.zIndex = 10001;
        }
    }

    function listQuestionModal() {
        const questionModal = document.getElementById('list-question-modal');
        const modalContainer = document.getElementById('list-question-modal-container');
        if (modalContainer.style.display === 'block') {
            questionModal.style.display = 'none';
            modalContainer.style.display = 'none';
        } else {
            modalContainer.style.display = 'block';
            questionModal.style.display = 'block';
            questionModal.style.zIndex = 10001;
        }
    }
    
    const listModalExit = document.getElementById('list-question-modal-exit');
    const listQuestion = document.getElementById('list-question');
    listQuestion.onclick = listQuestionModal;
    listModalExit.onclick = listQuestionModal;

    const modalLongExit = document.getElementById('long-question-modal-exit');
    const longFormQuestion = document.getElementById('long-question');
    longFormQuestion.onclick = longQuestionModal;
    modalLongExit.onclick = longQuestionModal;

    function dateModal() {
        const dateModal = document.getElementById('date-question-modal');
        const modalContainer = document.getElementById('date-question-modal-container');
        if (modalContainer.style.display === 'block') {
            dateModal.style.display = 'none';
            modalContainer.style.display = 'none';
        } else {
            modalContainer.style.display = 'block';
            dateModal.style.display = 'block';
            dateModal.style.zIndex = 10001;
        }
    }

    const dateModalExit = document.getElementById('date-question-modal-exit');
    const dateQuestion = document.getElementById('date-question');
    dateQuestion.onclick = dateModal;
    dateModalExit.onclick = dateModal;

    function addressModal() {
        const addressModal = document.getElementById('address-question-modal');
        const modalContainer = document.getElementById('address-question-modal-container');
        if (modalContainer.style.display === 'block') {
            addressModal.style.display = 'none';
            modalContainer.style.display = 'none';
        } else {
            modalContainer.style.display = 'block';
            addressModal.style.display = 'block';
            addressModal.style.zIndex = 10001;
        }
    }

    const addressModalExit = document.getElementById('address-question-modal-exit');
    const addressQuestion = document.getElementById('address-question');
    addressQuestion.onclick = addressModal;
    addressModalExit.onclick = addressModal;

    function pdfTextModal() {
        const pdfTextModal = document.getElementById('pdf-text-modal');
        const modalContainer = document.getElementById('pdf-text-modal-container');
        if (modalContainer.style.display === 'block') {
            pdfTextModal.style.display = 'none';
            modalContainer.style.display = 'none';
        } else {
            modalContainer.style.display = 'block';
            pdfTextModal.style.display = 'block';
            pdfTextModal.style.zIndex = 10001;
        }
    }

    const modalPDFExit = document.getElementById('pdf-text-modal-exit');
    const pdfText = document.getElementById('pdf-text');
    pdfText.onclick = pdfTextModal;
    modalPDFExit.onclick = pdfTextModal;


    ///////////////////////////// table configure 1/////////////////////////////

    function tableConfigure() {

        const tableConfigure = document.getElementById('table-configure-modal');
        const modalContainer = document.getElementById('table-configure-modal-container');

        if (modalContainer.style.display === 'block') {
            tableConfigure.style.display = 'none';
            modalContainer.style.display = 'none';
        } else {
            modalContainer.style.display = 'block';
            tableConfigure.style.display = 'block';
            tableConfigure.style.zIndex = 10003;
        }
    }
    
    let tableConfigureModalExit = document.getElementById('table-configure-modal-exit');
    let tableConfigureVar = document.getElementById('table-question');
    tableConfigureVar.onclick = tableConfigure;
    tableConfigureModalExit.onclick = tableConfigure;

    ///////////////////////////// table configure 2 /////////////////////////////

    function generate() {

        let tableHTML = ''
        const rowsNumber = parseInt(document.getElementById("table-rows").value);
        const columnsNumber = parseInt(document.getElementById("table-cols").value);
    
        for (let i = 1; i <= rowsNumber; i++) {
        let tr = '<tr>'
        let td = ''
    
            for (let j = 1; j <= columnsNumber; j++) {
        
                if (i === 1 || j === 1) {
                td = `<th><input type="text" placeholder="banana"/></th>`;
                }
                else {
                td = `<td><input type="text" placeholder="banana"/></td>`;
                }
        
                tr += td
            }
    
        tr += '</tr>'
        tableHTML += tr
        
    }

        const generateButton = document.getElementById('generate-table');
        generateButton.style.display = 'none';
        const tableObj = document.getElementById('table-output');
        tableObj.innerHTML = tableHTML
    }

    let generateButton = document.getElementById('generate-table');
    generateButton.onmouseover = generate;

}