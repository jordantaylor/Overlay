import os.path
import collections
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from GeoInfo import *

class QtImageViewer(QGraphicsView):
    
    add_delete_waypoint_signal = pyqtSignal(int, str, int, int)

    def __init__(self):

        # 'cur_path' is used to generate the paths for the .pngs
        self.cur_path = os.path.dirname(__file__)

        # 'key_array' holds the alphabetical ('A'-'Z') keys associated with the waypoints
        self.key_array = [] 
        for x in range(0, 26):
            self.key_array.append(chr(ord('Z') - x))

        # 'waypoints' holds all waypoints in LIFO order
        self.waypoints = collections.OrderedDict()

        # 'waypoint_icon' holds the pin .png as a pixmap
        self.waypoint_icon = QPixmap(os.path.join(self.cur_path, '../../assets/pin.png'))

        QGraphicsView.__init__(self)
        self.setRenderHints(QPainter.Antialiasing|QPainter.SmoothPixmapTransform)

        # 'vlayout' controls the vertical placement of the onscreen buttons
        self.vlayout = QBoxLayout(QBoxLayout.TopToBottom)
        self.vlayout.setAlignment(Qt.AlignTop|Qt.AlignRight)
        self.vlayout.addSpacing(80)

        zoom_in_btn = QPushButton()
        zoom_in_btn.setFixedSize(QSize(45, 45))
        zoom_in_btn.setIcon(QIcon(os.path.join(self.cur_path, '../../assets/zoom_in.png')))
        zoom_in_btn.setIconSize(QSize(35, 35))
        zoom_in_btn.setToolTip("zoom in to image")
        zoom_in_btn.clicked.connect(self.zoom_in_btn_press)
        self.vlayout.addWidget(zoom_in_btn)

        zoom_out_btn = QPushButton()
        zoom_out_btn.setFixedSize(QSize(45, 45))
        zoom_out_btn.setIcon(QIcon(os.path.join(self.cur_path, '../../assets/zoom_out.png')))
        zoom_out_btn.setIconSize(QSize(35, 35))
        zoom_out_btn.setToolTip("zoom out of image")
        zoom_out_btn.clicked.connect(self.zoom_out_btn_press)
        self.vlayout.addWidget(zoom_out_btn)

        expand_btn = QPushButton()
        expand_btn.setFixedSize(QSize(45, 45))
        expand_btn.setIcon(QIcon(os.path.join(self.cur_path, '../../assets/expand.png')))
        expand_btn.setIconSize(QSize(35, 35))
        expand_btn.setToolTip("reset zoom level")
        expand_btn.clicked.connect(self.expand_btn_press)
        self.vlayout.addWidget(expand_btn)

        visibility_wpts_btn = QPushButton()
        visibility_wpts_btn.setFixedSize(QSize(45, 45))
        visibility_wpts_btn.setIcon(QIcon(os.path.join(self.cur_path, '../../assets/visibility.png')))
        visibility_wpts_btn.setIconSize(QSize(35, 35))
        visibility_wpts_btn.setToolTip("hide/show all waypoints")
        visibility_wpts_btn.clicked.connect(self.visibility_wpts_btn_press)
        self.vlayout.addWidget(visibility_wpts_btn)

        undo_wpt_btn = QPushButton()
        undo_wpt_btn.setFixedSize(QSize(45, 45))
        undo_wpt_btn.setIcon(QIcon(os.path.join(self.cur_path, '../../assets/undo.png')))
        undo_wpt_btn.setIconSize(QSize(35, 35))
        undo_wpt_btn.setToolTip("undo last added waypoint")
        undo_wpt_btn.clicked.connect(self.undo_wpt_btn_press)
        self.vlayout.addWidget(undo_wpt_btn)

        self.setLayout(self.vlayout)

        # 'hlayout' controls the horizontal placement of the onscreen buttons
        self.hlayout = QHBoxLayout()
        self.hlayout.setAlignment(Qt.AlignRight)
        self.hlayout.addSpacing(110)
        self.vlayout.addLayout(self.hlayout)

    # 'set_image' is called by 'OverlayWidget' to set the .tif image
    def set_image(self, str):
        self.image_path = str
        self.pixmap = QPixmap(self.image_path)
        self.scene = QGraphicsScene()
        self.scene.addPixmap(self.pixmap)
        self.setScene(self.scene)
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.gps_points = get_points(self.image_path)
        self.create_grid()

    def create_grid(self):
        lines = compute_gridlines( self.gps_points )
        major = QPen()
        major.setWidth(3)
        major.setCosmetic(True)
        major.setBrush(Qt.red)
        minor = QPen()
        minor.setWidth(2)
        minor.setCosmetic(True)
        minor.setBrush(Qt.red)
        minor.setStyle(Qt.DashLine)
        self.add_waypoint(23006, 16192)
        self.add_waypoint(16192, 23006)
        for line in lines: # line : [ [ x1, y1, x2, y2 ] ]
            if line[1]:
                self.scene.addLine( line[0], major )
            else:
                self.scene.addLine( line[0], minor )
            print(line[0])

    def zoom_in_btn_press(self):
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.scale(1.25, 1.25)

    def zoom_out_btn_press(self):
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.scale(0.8, 0.8)

    def expand_btn_press(self):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def visibility_wpts_btn_press(self):
        if self.waypoints and self.waypoints[list(self.waypoints.keys())[0]].isVisible():
            for x in self.waypoints:
                self.waypoints[x].hide()
        else:
            for x in self.waypoints:
                self.waypoints[x].show()

    def undo_wpt_btn_press(self):
        if self.waypoints:
            self.add_delete_waypoint_signal.emit(0, list(self.waypoints.keys())[-1])

    # 'delete_waypoint' deletes the specified waypoint if it exists
    def delete_waypoint(self, _key):
        if self.waypoints and _key not in self.key_array:
            self.scene.removeItem(self.waypoints[_key])
            self.key_array.append(_key)
            del self.waypoints[_key]

    # 'add_waypoint' adds a waypoint to the image if there are remaining keys in the 'key_array'
    def add_waypoint(self, x, y):
        if self.key_array: 
            self.waypoint = QGraphicsPixmapItem(self.waypoint_icon)
            self.waypoint.setPos(x, y)
            self.scene.addItem(self.waypoint)
            _key = self.key_array.pop()
            self.waypoints[_key] = self.waypoint
            self.add_delete_waypoint_signal.emit(1, _key, x, y)

    # 'wheelEvent' is used for scroll zooming the image
    def wheelEvent(self, event):
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 0.8
        self.scale(factor, factor)

    # 'mousePressEvent' is used for panning of the image and adding waypoints
    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        if event.button() == Qt.RightButton:
            self.add_waypoint(scenePos.x(), scenePos.y() - self.waypoint_icon.height())
        else:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        QGraphicsView.mousePressEvent(self, event)

    # 'mouseReleaseEvent' is used to stop panning of the image upon mouse release
    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)