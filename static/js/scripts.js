setTimeout(function() {
    let alert = document.querySelector('.alert');
    if (alert) {
        alert.classList.remove('show');
        alert.classList.add('fade');
        setTimeout(function() {
            alert.remove();
        }, 500);
    }
}, 3000);


document.addEventListener('DOMContentLoaded', function() {
    const addOptionButton = document.getElementById('add-option');
    const removeOptionButton = document.getElementById('remove-option');
    const optionsContainer = document.getElementById('options-container');
    let optionCount = 2;

    function updateRemoveButtonState() {
        const optionRows = optionsContainer.querySelectorAll('.option-row');
        removeOptionButton.disabled = optionRows.length <= 2;
    }

    addOptionButton.addEventListener('click', function() {
        optionCount++;
        const newOption = document.createElement('div');
        newOption.classList.add('mb-3', 'option-row');
        newOption.innerHTML = `
            <label for="option_${optionCount}" class="form-label">Seçenek ${optionCount}</label>
            <input type="text" class="form-control" id="option_${optionCount}" name="option_${optionCount}" required>
            <input type="radio" name="answer" value="${optionCount}" required> <span class="text-success">Doğru Cevap</span>
        `;
        optionsContainer.appendChild(newOption);
        updateRemoveButtonState();
    });

    removeOptionButton.addEventListener('click', function() {
        const optionRows = optionsContainer.querySelectorAll('.option-row');
        if (optionRows.length > 2) { 
            optionCount--;
            optionsContainer.removeChild(optionRows[optionRows.length - 1]);
            updateRemoveButtonState();
        }
    });

    updateRemoveButtonState();
});
