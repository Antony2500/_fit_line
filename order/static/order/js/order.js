document.addEventListener('DOMContentLoaded', function() {
    // Найдите поле ввода номера телефона по его атрибуту name
    var mobileInput = document.querySelector('input[name="mobile"]');


    mobileInput.addEventListener('input', function() {
        // Получите текущее значение поля ввода
        var currentValue = this.value;

        // Проверьте, начинается ли текущее значение с "+380"
        if (!currentValue.startsWith('+380')) {
            // Если нет, добавьте "+380" к началу
            this.value = '+380' + currentValue;
        }

    });

    // Добавьте обработчик события нажатия клавиши
    mobileInput.addEventListener('keydown', function(e) {
        // Получите код нажатой клавиши
        var keyCode = e.keyCode || e.which;

        // Получите текущее значение поля ввода
        var currentValue = this.value;

        // Если нажата клавиша "Backspace" и текущее значение не начинается с "+380"
        if (keyCode === 8 && !currentValue.startsWith('+380')) {
            // Предотвратите выполнение события
            e.preventDefault();
        }
    });
});

