const slider = document.getElementById('slider');
    noUiSlider.create(slider, {
      start: [0, 5000],
      connect: true,
      range: {
        'min': 0,
        'max': 5000
      },
      step: 1.5
    });

    const minValue = document.getElementById('price_min');
    const maxValue = document.getElementById('price_max');

    slider.noUiSlider.on('update', function (values) {
      minValue.value = values[0];
      maxValue.value = values[1];
    });