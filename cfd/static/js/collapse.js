// Copy of https://github.com/django/django/blob/master/django/contrib/admin/static/admin/js/collapse.js
// with minor adjustments
var closestElem = function(elem, tagName) {
    if (elem.nodeName === tagName.toUpperCase()) {
        return elem;
    }
    if (elem.parentNode.nodeName === 'BODY') {
        return null;
    }
    return elem.parentNode && closestElem(elem.parentNode, tagName);
};

/*global gettext*/
(function() {
    'use strict';
    window.addEventListener('load', function() {
        // Add anchor tag for Show/Hide link
        var fieldsets = document.querySelectorAll('fieldset.collapse');
        for (var i = 0; i < fieldsets.length; i++) {
            var elem = fieldsets[i];
            // Don't hide if fields in this fieldset have errors
            if (elem.querySelectorAll('div.errors').length === 0) {
                elem.classList.add('collapsed');
                var h2 = elem.querySelector('h2');
                
                if (h2.classList.contains('blank')){
                    break
                }
                
                var link = document.createElement('a');
                link.setAttribute('id', 'fieldsetcollapser' + i);
                link.setAttribute('class', 'collapse-toggle');
                link.setAttribute('href', '#');
                link.textContent = gettext('Show');
                h2.appendChild(document.createTextNode(' ('));
                h2.appendChild(link);
                h2.appendChild(document.createTextNode(')'));

                
                h2.addEventListener('click', function(ev){     
                    this.querySelector('a').click()                              
                 });
            }
        }
        // Add toggle to anchor tag
        var toggles = document.querySelectorAll('fieldset.collapse a.collapse-toggle');
        var toggleFunc = function(ev) {            
            ev.preventDefault();
            var fieldset = closestElem(this, 'fieldset');
            if (fieldset.classList.contains('collapsed')) {
                // Show
                this.textContent = gettext('Hide');
                fieldset.classList.remove('collapsed');
            } else {
                // Hide
                this.textContent = gettext('Show');
                fieldset.classList.add('collapsed');
            }
            
            ev.stopPropagation()
        };
        for (i = 0; i < toggles.length; i++) {
            toggles[i].addEventListener('click', toggleFunc);
        }

        var showParentFieldset = function(elemList){
            for (var count = 0; count < elemList.length; count++){
                var fieldset = closestElem(elemList[count], 'fieldset'); 
                fieldset = document.getElementsByClassName(fieldset.classList.value)[0];
    
                if (fieldset.classList.contains('collapsed')){ 
    
                    var header = fieldset.querySelector('h2');
                    if (!header.classList.contains('blank')){
                        header.querySelector('a').click();
                    }         
                           
                }
                
            }
        }
        
        var fieldErrors = document.getElementsByClassName('fieldset-input-error');
        var changedFields = document.getElementsByClassName('fieldset-field-changed');
        
        showParentFieldset(fieldErrors);
        showParentFieldset(changedFields);
    });
})();