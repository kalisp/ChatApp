import QtQuick 2.12
import QtQuick.Window 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.2


ApplicationWindow {
    id : window
    visible: true
    //visibility: Window.FullScreen
    width: Screen.width
    height: Screen.height - 100

    color: 'darkgrey'

    SplitView {
        anchors.fill: parent

        // room list column + private convo
        ColumnLayout {
            id: left_column
            SplitView.preferredWidth: 100

            ListView {
                anchors.fill: parent //TODO shouldnt be there, but Layout.fillWidth: true just doesnt work

                clip: true
                model: room_model
                spacing: 2
                delegate: room_delegate
            }
            Component {
                id: room_delegate

                Rectangle {
                    width: ListView.view.width
                    height: 40

                    color: ListView.isCurrentItem?"#157efb":"#53d769"
                    border.color: Qt.lighter(color, 1.1)

                    Text {
                        id: text_item
                        anchors.centerIn: parent
                        font.pixelSize: 10
                        text: model.name_role
                    }

                    MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                console.log("Click!" + model.id_role)
                                //model.get_rooms()
                            }
                        }
                }


            }
        }

        // central column - post list +  send post
        ColumnLayout {
            SplitView.fillWidth: true
            Layout.minimumHeight: parent.height
            //Layout.minimumWidth: Screen.width - left_column.width - 100

            ListView {
                id: post_list
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                model: post_model
                delegate: post_delegate
                verticalLayoutDirection: ListView.BottomToTop
                Layout.margins: 2
            }

            Component {
                id: post_delegate

                Rectangle {
                    width: ListView.view.width
                    height: 40
                    //color: ListView.isCurrentItem?"#157efb":"#53d769"
                    //border.color: Qt.lighter(color, 1.1)

                    Text {
                        font.pixelSize: 16
                        Layout.alignment : Qt.AlignLeft
                        Layout.leftMargin: 5
                        text: model.display
                    }
                }
            }

            Pane {
                Layout.fillWidth: true
                RowLayout {
                    width: parent.width
                    Layout.alignment: Qt.AlignBaseline

                    TextArea {
                        id: messageField
                        Layout.alignment : Qt.AlignLeft
                        Layout.leftMargin: 10
                        placeholderText: qsTr("Compose message")
                        wrapMode: TextArea.Wrap
                    }

                    Button {
                        id: sendButton
                        Layout.alignment : Qt.AlignRight
                        Layout.rightMargin: 10
                        text: qsTr("Send")
                        enabled: messageField.length > 0
                    }
                }
            }
        }


        // right column - search + search results
        Rectangle {
            id: right_column
            SplitView.preferredWidth: 100
            color: "lightgreen"
            Text {
                text: "View 3"
                anchors.centerIn: parent
            }
        }
   }
}


