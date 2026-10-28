// 1. Zmiana pacjenta w panelu bocznym
const patientCards = document.querySelectorAll('.patient-card');
const breadcrumbs = document.getElementById('breadcrumbs');

patientCards.forEach(card => {
    card.addEventListener('click', function() {
        // Usuń klasę active ze wszystkich
        patientCards.forEach(c => c.classList.remove('active'));
        // Dodaj do klikniętego
        this.classList.add('active');
        
        // Zaktualizuj okruszki (breadcrumbs) na górze
        const name = this.getAttribute('data-name');
        const date = this.getAttribute('data-date');
        breadcrumbs.innerHTML = `Pacjenci / ${name} / <strong>Analiza RTG - ${date}</strong>`;
    });
});

// 2. Obsługa przycisku "Zapisz w Bazie"
const btnSave = document.getElementById('btnSave');
btnSave.addEventListener('click', function() {
    const originalText = this.innerText;
    this.innerText = 'Zapisano pomyślnie ✓';
    this.classList.add('btn-success-state');
    this.disabled = true;

    setTimeout(() => {
        this.innerText = originalText;
        this.classList.remove('btn-success-state');
        this.disabled = false;
    }, 2000);
});

// 3. Obsługa przycisku "Eksportuj Raport"
const btnExport = document.getElementById('btnExport');
btnExport.addEventListener('click', function() {
    alert('Rozpoczęto generowanie pliku PDF z raportem z analizy AI. Plik zostanie pobrany za chwilę.');
});

// 4. Obsługa przycisku "Przelicz symulację"
const btnSimulate = document.getElementById('btnSimulate');
const line = document.getElementById('correctionLine');
const angleLeft = document.getElementById('angleLeft');
const rotationValue = document.getElementById('rotationValue');

btnSimulate.addEventListener('click', function() {
    const originalText = this.innerText;
    this.innerText = 'Przeliczanie modelu AI... ⏳';
    this.disabled = true;
    this.style.opacity = '0.7';
    
    // Animacja linii (symulacja szukania lepszego kąta)
    line.style.transform = 'rotate(-5deg)';
    line.style.transition = 'transform 1s ease-in-out';

    setTimeout(() => {
        this.innerText = 'Zakończono ✓';
        this.style.background = '#36b37e';
        
        // Aktualizacja danych po "przeliczeniu"
        line.style.transform = 'rotate(-18deg)';
        angleLeft.innerText = '105°';
        angleLeft.classList.remove('danger');
        angleLeft.classList.add('success');
        rotationValue.innerText = '18 stopni';

        setTimeout(() => {
            this.innerText = originalText;
            this.disabled = false;
            this.style.opacity = '1';
            this.style.background = '#42526e'; // powrót do domyślnego koloru
        }, 2000);
    }, 1500);
});

// 5. Aktywacja narzędzi (lupka, miarka)
function toggleTool(element) {
    element.classList.toggle('active-tool');
}

// 6. Ukrywanie/Pokazywanie wektorów AI na zdjęciu
function toggleVisibility(element) {
    element.classList.toggle('active-tool');
    const overlayLine = document.getElementById('correctionLine');
    if (overlayLine.style.display === 'none') {
        overlayLine.style.display = 'block';
        element.style.opacity = '1';
    } else {
        overlayLine.style.display = 'none';
        element.style.opacity = '0.4';
    }
}