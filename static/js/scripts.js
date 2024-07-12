document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('predictForm');
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const submitButton = form.querySelector('input[type="submit"]');
        submitButton.disabled = true;

        const text = document.getElementById('text').value;

        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            if (data.prediction) {
                if (data.prediction === "spam") {
                    resultDiv.innerHTML = `<span class="spam">Prédiction : ${data.prediction}</span>`;
                } else {
                    resultDiv.innerHTML = `<span class="ham">Prédiction : ${data.prediction}</span>`;
                }
            } else {
                resultDiv.textContent = `Erreur : ${data.error}`;
            }
            submitButton.disabled = false; // Réactive le bouton
        })
        .catch(error => {
            console.error('Erreur:', error);
            submitButton.disabled = false; // Réactive le bouton même en cas d'erreur
        });
    });

    // Ajouter des événements supplémentaires ici
    const textArea = document.getElementById('text');
    textArea.addEventListener('focus', function() {
        textArea.style.backgroundColor = '#e0f7fa';
    });

    textArea.addEventListener('blur', function() {
        textArea.style.backgroundColor = '';
    });
});



document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('.update-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            const formData = new FormData(form);

            fetch('/update_prediction', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Annotation mise à jour avec succès');
                } else {
                    alert('Erreur lors de la mise à jour de l\'annotation');
                }
                submitButton.disabled = false;
            })
            .catch(error => {
                console.error('Erreur:', error);
                submitButton.disabled = false;
            });
        });
    });
});
