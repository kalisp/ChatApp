import QtQuick 2.12
import QtQuick.Window 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.2

ApplicationWindow {
    id : window
    visible: true
    width: Screen.width
    height: Screen.height - 100
    //flags: Qt.FramelessWindowHint

    property color backGroundColor : "#394454"
    property color mainAppColor: "#6fda9c" //"#FA6B65"
    property color mainTextCOlor: "#f0f0f0"

    FontLoader {
        id: fontAwesome
        name: "fontawesome"
        source: "fontawesome-webfont.ttf"
    }

    // Main stackview
    StackView{
        id: stackView
        focus: true
        anchors.fill: parent
    }

    Component.onCompleted: {
        stackView.push("login_page.qml")   //initial page
        console.log('login_page')
    }

    Popup {
        id: popup
        property alias popMessage: message.text
        background: Rectangle {
            implicitWidth: window.width - 200
            implicitHeight: 60
            color: "#b44"
        }

        y: window.height
        modal: true
        focus: true
        closePolicy: Popup.CloseOnPressOutside

        Text {
            id: message
            anchors.centerIn: parent
            font.pointSize: 12
            color: "#ffffff"
        }

        onOpened: popupClose.start()
    }

    // Popup will be closed automatically in 2 seconds after its opened
    Timer {
        id: popupClose
        interval: 5000
        onTriggered: popup.close()
    }
}
