$(function () {
    $(".table-responsive").responsiveTable({
        //addDisplayAllBtn: "btn btn-secondary",
        addDisplayAllBtn:false,
        addFocusBtn:false,
    }), $(".btn-toolbar [data-toggle=dropdown]").attr("data-bs-toggle", "dropdown")
});