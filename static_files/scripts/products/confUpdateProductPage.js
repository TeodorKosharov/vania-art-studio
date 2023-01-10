document.querySelectorAll('button')[1].textContent = 'Редактирай';
document.querySelector('input[name="owner_id"]').type = 'hidden';
const imgFieldInfo = document.querySelector('.img-field').children[1];
const imgFieldDiv = document.querySelector('.img-field');
const imgAnchor = imgFieldInfo.children[0];
const imgInput = imgFieldInfo.children[2];

imgFieldInfo.remove();

imgAnchor.textContent = 'Текущо изображение';
imgAnchor.className = 'current-image-anchor';
imgFieldDiv.append(document.createElement('p'));
imgFieldDiv.append(imgAnchor);
imgFieldDiv.append(imgInput);