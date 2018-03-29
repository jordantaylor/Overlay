import os.path
import collections
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from GeoInfo import *

class QtImageViewer(QGraphicsView):
    
    # 'add_delete_waypoint_signal' is used to communicate with the class 'OverlayWidget'
    add_delete_waypoint_signal = pyqtSignal(int, str, int, int)

    def __init__(self):

        ###################################
        # Initialize variables
        ###################################
        # 'cur_path' is used to generate the paths for the images used within the image viewer
        self.cur_path = os.path.dirname(__file__)

        # the following variables are used to scale the image
        self.zoom_max = 15
        self.zoom_min = -2
        self.zoom_level = 0

        # the following variables are used to scale waypoints with relation to the image
        self.wpt_cur_scale = 2.0
        self.wpt_def_scale = 2.0
        self.wpt_max_scale = 2.0
        self.wpt_min_scale = 0.5
        self.wpt_scale_factor = 0.5

        # 'key_array' holds the alphabetical keys associated with each waypoint
        # 'key_array' is in the order Z through A
        self.key_array = [] 
        for x in range(0, 26):
            self.key_array.append(chr(ord('Z') - x))

        # 'waypoints' holds all waypoints in the order that they are added to the screen
        self.waypoints = collections.OrderedDict()

        ###################################
        # Create the image viewer
        ###################################

        QGraphicsView.__init__(self)
        self.setRenderHints(QPainter.Antialiasing|QPainter.SmoothPixmapTransform)

        # 'vlayout' controls the vertical placement of the onscreen buttons
        self.vlayout = QBoxLayout(QBoxLayout.TopToBottom)
        self.vlayout.setAlignment(Qt.AlignTop|Qt.AlignRight)

        self.init_navbtns()
        self.setLayout(self.vlayout)

        # 'hlayout' controls the horizontal placement of the onscreen buttons
        self.hlayout = QHBoxLayout()
        self.hlayout.setAlignment(Qt.AlignRight)
        self.hlayout.addSpacing(50)
        self.vlayout.addLayout(self.hlayout)

        # 'hlayout' controls the horizontal placement of the onscreen buttons
        self.hlayout = QHBoxLayout()
        self.hlayout.setAlignment(Qt.AlignRight)
        self.hlayout.addSpacing(110)
        self.vlayout.addLayout(self.hlayout)
        
        self.setLayout(self.vlayout)
        
    # set up all of the nav buttons that appear over the map
    def init_navbtns(self):
        zoom_in_btn = QPushButton()
        zoom_in_btn.setFixedSize(QSize(35, 35))
        zoom_in_btn.setIcon(QIcon(os.path.join(self.cur_path, '../../assets/zoom_in.png')))
        zoom_in_btn.setIconSize(QSize(25, 25))
        zoom_in_btn.setToolTip("zoom in to image")
        zoom_in_btn.clicked.connect(self.zoom_in_btn_press)
        self.vlayout.addWidget(zoom_in_btn)

        zoom_out_btn = QPushButton()
        zoom_out_btn.setFixedSize(QSize(35, 35))
        zoom_out_btn.setIcon(QIcon(os.path.join(self.cur_path, '../../assets/zoom_out.png')))
        zoom_out_btn.setIconSize(QSize(25, 25))
        zoom_out_btn.setToolTip("zoom out of image")
        zoom_out_btn.clicked.connect(self.zoom_out_btn_press)
        self.vlayout.addWidget(zoom_out_btn)

        expand_btn = QPushButton()
        expand_btn.setFixedSize(QSize(35, 35))
        expand_btn.setIcon(QIcon(os.path.join(self.cur_path, '../../assets/expand.png')))
        expand_btn.setIconSize(QSize(25, 25))
        expand_btn.setToolTip("reset zoom level")
        expand_btn.clicked.connect(self.expand_btn_press)
        self.vlayout.addWidget(expand_btn)

        visibility_wpts_btn = QPushButton()
        visibility_wpts_btn.setFixedSize(QSize(35, 35))
        visibility_wpts_btn.setIcon(QIcon(os.path.join(self.cur_path, '../../assets/visibility.png')))
        visibility_wpts_btn.setIconSize(QSize(25, 25))
        visibility_wpts_btn.setToolTip("hide/show all waypoints")
        visibility_wpts_btn.clicked.connect(self.visibility_wpts_btn_press)
        self.vlayout.addWidget(visibility_wpts_btn)

        undo_wpt_btn = QPushButton()
        undo_wpt_btn.setFixedSize(QSize(35, 35))
        undo_wpt_btn.setIcon(QIcon(os.path.join(self.cur_path, '../../assets/undo.png')))
        undo_wpt_btn.setIconSize(QSize(25, 25))
        undo_wpt_btn.setToolTip("undo last added waypoint")
        undo_wpt_btn.clicked.connect(self.undo_wpt_btn_press)
        self.vlayout.addWidget(undo_wpt_btn)

    ###################################
    # Helper functions
    ###################################

    # 'set_image' is called by 'OverlayWidget' to add the .tif image to the image viewer
    def set_image(self, str):
        self.image_path = str
        self.pixmap = QPixmap(self.image_path)
        self.scene = QGraphicsScene()
        self.scene.addPixmap(self.pixmap)
        self.setScene(self.scene)
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.gps_points = get_points(self.image_path)
        self.create_grid()

        #self.setSceneRect(self.sceneRect().x(), self.sceneRect().y(), self.sceneRect().width() + 1000, self.sceneRect().height() + 1000)

    def create_grid(self):
        lines = compute_gridlines( self.gps_points )
        major = QPen()
        major.setWidth(2)
        major.setCosmetic(True)
        major.setBrush(Qt.red)
        minor = QPen()
        minor.setWidth(1)
        minor.setCosmetic(True)
        minor.setBrush(Qt.red)
        minor.setStyle(Qt.DashLine)
        for line in lines: # line : [ [ x1, y1, x2, y2 ] ]
            if line[1]:
                self.scene.addLine( line[0], major )
            else:
                self.scene.addLine( line[0], minor )
            print(line[0])

    # 'zoom_in' handles the zooming of the image and the related scaling of the waypoints
    def zoom_in(self):
        if self.zoom_level < self.zoom_max:
            self.scale(1.25, 1.25)
            self.zoom_level += 1
            if self.wpt_cur_scale > self.wpt_min_scale:
                self.wpt_cur_scale -= self.wpt_scale_factor
            if self.waypoints:
                for key, val in self.waypoints.items():
                    val.setScale(self.wpt_cur_scale)

    # 'zoom_out' handles the zooming of the image and the related scaling of the waypoints
    def zoom_out(self):
        if self.zoom_level > self.zoom_min:
            self.scale(0.8, 0.8)
            self.zoom_level -= 1
            if self.wpt_cur_scale < self.wpt_max_scale:
                self.wpt_cur_scale += self.wpt_scale_factor
            if self.waypoints:
                for key, val in self.waypoints.items():
                    val.setScale(self.wpt_cur_scale)

    # 'delete_waypoint' deletes the specified waypoint if it exists
    def delete_waypoint(self, _key):
        if self.waypoints and _key not in self.key_array:
            self.scene.removeItem(self.waypoints[_key])
            self.key_array.append(_key)

            self.key_array.sort(reverse = True)
            del self.waypoints[_key]

    # 'add_waypoint' adds a waypoint to the image if there are less than 26 on screen
    def add_waypoint(self, x, y):
        if self.key_array:
            _key = self.key_array.pop()
            _alpha_pin_path = '../../assets/pins/pin_' + _key + '.png'
            self.waypoint_icon = QPixmap(os.path.join(self.cur_path, _alpha_pin_path))
            self.waypoint = QGraphicsPixmapItem(self.waypoint_icon)
            self.waypoint.setTransformOriginPoint(0, self.waypoint_icon.height())
            self.waypoint.setPos(x, y - self.waypoint_icon.height())
            self.waypoint.setScale(self.wpt_cur_scale)
            self.scene.addItem(self.waypoint)
            self.waypoints[_key] = self.waypoint
            self.add_delete_waypoint_signal.emit(1, _key, x, y - self.waypoint_icon.height())

    ###################################
    # Button press functions
    ###################################

    def zoom_in_btn_press(self):
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.zoom_in()

    def zoom_out_btn_press(self):
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.zoom_out()

    def expand_btn_press(self):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.zoom_level = 0
        if self.waypoints:
            self.wpt_cur_scale = self.wpt_def_scale
            for key, val in self.waypoints.items():
                val.setScale(self.wpt_def_scale)

    def visibility_wpts_btn_press(self):
        if self.waypoints and self.waypoints[list(self.waypoints.keys())[0]].isVisible():
            for x in self.waypoints:
                self.waypoints[x].hide()
        else:
            for x in self.waypoints:
                self.waypoints[x].show()

    def undo_wpt_btn_press(self):
        if self.waypoints:
            self.add_delete_waypoint_signal.emit(0, list(self.waypoints.keys())[-1], 0, 0)

    ###################################
    # Mouse interaction functions
    ###################################

    # 'wheelEvent' is used to register zooming of the image with the mouse scroll wheel
    def wheelEvent(self, event):
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    # 'mousePressEvent' is to register panning of the image with the left mouse button
    # 'mousePressEvent' is to register the adding of waypoints with the right mouse button
    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        if event.button() == Qt.RightButton:
            self.add_waypoint(scenePos.x(), scenePos.y())
        else:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        QGraphicsView.mousePressEvent(self, event)

    # 'mouseReleaseEvent' is used to stop the panning of the image upon the release of the left mouse button
    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)

#########################################################################################