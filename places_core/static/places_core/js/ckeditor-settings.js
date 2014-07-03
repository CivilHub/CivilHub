// CKEDITOR configuration options
window.CONFIG = window.CONFIG || {};
// Przykładowa konfiguracja panelu z uwzględnieniem wszystkich możliwych
// elementów (za wyjątkiem customowych pluginów naszej produkcji):
// http://s1.ckeditor.com/sites/default/files/uploads/Complete%20List%20of%20Toolbar%20Items%20for%20CKEditor.pdf
window.CONFIG.ckeditor = {
    // Domyślna konfiguracja (pełny edytor) do wykorzystania w artykułach
    // i generalnie tam, gdzie potrzebne są bardziej zaawansowane funkcje
    // edycji.
    'default': {},
    // Minimalna konfiguracja, ale z zachowaniem przycisku dodawania mediów
    // (i w przyszłości innych customowych plug-inów).
    'custom': {
        toolbar: [
            { name: 'document', items: [ 'Source' ] },
            [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ],
            { name: 'basicstyles', items: [ 'Bold', 'Italic' ] },
            { name: 'plugins', items: [ 'MediaUploader' ]},
        ],
        allowedContent: true
    },
    // Absolutnie minimalna konfiguracja - do dyskusji etc. gdzie nie wstawia
    // się obrazków, za to potrzebny jest plugin BB-Code itp.
    'minimal': {
        toolbar: [
            { name: 'basicstyles', items: [ 'Bold', 'Italic' ] }
        ],
        removePlugins: 'elementspath'
    }
};