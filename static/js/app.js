// Función para mostrar resultados
function showResult(message, type) {
    const resultDiv = document.getElementById('result');
    resultDiv.textContent = message;
    resultDiv.className = type;
    resultDiv.style.display = 'block';
}

// Función para resetear el botón
function resetButton() {
    document.getElementById('buttonText').style.display = 'inline';
    document.getElementById('loadingSpinner').style.display = 'none';
    document.getElementById('sendButton').disabled = false;
}

// Validación en tiempo real (solo números)
document.querySelectorAll('.phone-input').forEach(input => {
    input.addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '');
    });
});

// Manejo del formulario
document.getElementById('inviteForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const sendButton = document.getElementById('sendButton');
    const buttonText = document.getElementById('buttonText');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // Mostrar estado de carga
    buttonText.style.display = 'none';
    loadingSpinner.style.display = 'inline';
    sendButton.disabled = true;

    const resultDiv = document.getElementById('result');
    resultDiv.style.display = 'none';

    // Obtener números válidos (8 dígitos)
    const numbers = [];
    for (let i = 1; i <= 5; i++) {
        const input = document.getElementById(`phone${i}`);
        if (input.value && input.checkValidity()) {
            numbers.push(input.value);
        }
    }

    if (numbers.length === 0) {
        showResult('Error: Debes ingresar al menos un número válido de 8 dígitos', 'error');
        resetButton();
        return;
    }

    try {
        const response = await fetch('/send_invitation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ numbers })
        });

        const data = await response.json();

        if (response.ok) {
            showResult(`✅ Se enviaron invitaciones a ${numbers.length} contacto(s)`, 'success');
            // Limpiar campos exitosos
            for (let i = 1; i <= 5; i++) {
                const input = document.getElementById(`phone${i}`);
                if (input.value && input.checkValidity()) {
                    input.value = '';
                }
            }
        } else {
            showResult(`❌ Error: ${data.error || 'Ocurrió un problema al enviar'}`, 'error');
        }
    } catch (error) {
        showResult(`❌ Error de conexión: ${error.message}`, 'error');
    } finally {
        resetButton();
    }
});