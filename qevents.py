# qevent lookup
from PyQt5.QtCore import QEvent

CODE_LOOKUP = {
    0: {
        "code": 0,
        "name": "None",
        "description": "Not an event."
    },

    114: {
        "code": 114,
        "name": "ActionAdded",
        "description": "A new action has been added (QActionEvent)."
    },
    113: {
        "code": 113,
        "name": "ActionChanged",
        "description": "An action has been changed (QActionEvent)."
    },
    115: {
        "code": 115,
        "name": "ActionRemoved",
        "description": "An action has been removed (QActionEvent)."
    },
    99: {
        "code": 99,
        "name": "ActivationChange",
        "description": "A widget's top-level window activation state has changed."
    },
    121: {
        "code": 121,
        "name": "ApplicationActivate",
        "description": "This enum has been deprecated. Use ApplicationStateChange instead."
    },
    122: {
        "code": 122,
        "name": "ApplicationDeactivate",
        "description": "This enum has been deprecated. Use ApplicationStateChange instead."
    },
    36: {
        "code": 36,
        "name": "ApplicationFontChange",
        "description": "The default application font has changed."
    },
    37: {
        "code": 37,
        "name": "ApplicationLayoutDirectionChange",
        "description": "The default application layout direction has changed."
    },
    38: {
        "code": 38,
        "name": "ApplicationPaletteChange",
        "description": "The default application palette has changed."
    },
    214: {
        "code": 214,
        "name": "ApplicationStateChange",
        "description": "The state of the application has changed."
    },
    35: {
        "code": 35,
        "name": "ApplicationWindowIconChange",
        "description": "The application's icon has changed."
    },
    68: {
        "code": 68,
        "name": "ChildAdded",
        "description": "An object gets a child (QChildEvent)."
    },
    69: {
        "code": 69,
        "name": "ChildPolished",
        "description": "A widget child gets polished (QChildEvent)."
    },
    71: {
        "code": 71,
        "name": "ChildRemoved",
        "description": "An object loses a child (QChildEvent)."
    },
    40: {
        "code": 40,
        "name": "Clipboard",
        "description": "The clipboard contents have changed."
    },
    19: {
        "code": 19,
        "name": "Close",
        "description": "Widget was closed (QCloseEvent)."
    },
    20: {
        "code": 20,
        "name": "Quit",
        "description": "Application was quit."
    },
    200: {
        "code": 200,
        "name": "CloseSoftwareInputPanel",
        "description": "A widget wants to close the software input panel (SIP)."
    },
    178: {
        "code": 178,
        "name": "ContentsRectChange",
        "description": "The margins of the widget's content rect changed."
    },
    82: {
        "code": 82,
        "name": "ContextMenu",
        "description": "Context popup menu (QContextMenuEvent)."
    },
    183: {
        "code": 183,
        "name": "CursorChange",
        "description": "The widget's cursor has changed."
    },
    52: {
        "code": 52,
        "name": "DeferredDelete",
        "description": "The object will be deleted after it has cleaned up (QDeferredDeleteEvent)"
    },
    60: {
        "code": 60,
        "name": "DragEnter",
        "description": "The cursor enters a widget during a drag and drop operation (QDragEnterEvent)."
    },
    62: {
        "code": 62,
        "name": "DragLeave",
        "description": "The cursor leaves a widget during a drag and drop operation (QDragLeaveEvent)."
    },
    61: {
        "code": 61,
        "name": "DragMove",
        "description": "A drag and drop operation is in progress (QDragMoveEvent)."
    },
    63: {
        "code": 63,
        "name": "Drop",
        "description": "A drag and drop operation is completed (QDropEvent)."
    },
    170: {
        "code": 170,
        "name": "DynamicPropertyChange",
        "description": "A dynamic property was added, changed, or removed from the object."
    },
    98: {
        "code": 98,
        "name": "EnabledChange",
        "description": "Widget's enabled state has changed."
    },
    10: {
        "code": 10,
        "name": "Enter",
        "description": "Mouse enters widget's boundaries (QEnterEvent)."
    },
    150: {
        "code": 150,
        "name": "EnterEditFocus",
        "description": "An editor widget gains focus for editing. QT_KEYPAD_NAVIGATION must be defined."
    },
    124: {
        "code": 124,
        "name": "EnterWhatsThisMode",
        "description": "Send to toplevel widgets when the application enters \"What's This?\" mode."
    },
    206: {
        "code": 206,
        "name": "Expose",
        "description": "Sent to a window when its on-screen contents are invalidated and need to be flushed from the backing store."
    },
    116: {
        "code": 116,
        "name": "FileOpen",
        "description": "File open request (QFileOpenEvent)."
    },
    8: {
        "code": 8,
        "name": "FocusIn",
        "description": "Widget or Window gains keyboard focus (QFocusEvent)."
    },
    9: {
        "code": 9,
        "name": "FocusOut",
        "description": "Widget or Window loses keyboard focus (QFocusEvent)."
    },
    23: {
        "code": 23,
        "name": "FocusAboutToChange",
        "description": "Widget or Window focus is about to change (QFocusEvent)"
    },
    97: {
        "code": 97,
        "name": "FontChange",
        "description": "Widget's font has changed."
    },
    198: {
        "code": 198,
        "name": "Gesture",
        "description": "A gesture was triggered (QGestureEvent)."
    },
    202: {
        "code": 202,
        "name": "GestureOverride",
        "description": "A gesture override was triggered (QGestureEvent)."
    },
    188: {
        "code": 188,
        "name": "GrabKeyboard",
        "description": "Item gains keyboard grab (QGraphicsItem only)."
    },
    186: {
        "code": 186,
        "name": "GrabMouse",
        "description": "Item gains mouse grab (QGraphicsItem only)."
    },
    159: {
        "code": 159,
        "name": "GraphicsSceneContextMenu",
        "description": "Context popup menu over a graphics scene (QGraphicsSceneContextMenuEvent)."
    },
    164: {
        "code": 164,
        "name": "GraphicsSceneDragEnter",
        "description": "The cursor enters a graphics scene during a drag and drop operation (QGraphicsSceneDragDropEvent)."
    },
    166: {
        "code": 166,
        "name": "GraphicsSceneDragLeave",
        "description": "The cursor leaves a graphics scene during a drag and drop operation (QGraphicsSceneDragDropEvent)."
    },
    165: {
        "code": 165,
        "name": "GraphicsSceneDragMove",
        "description": "A drag and drop operation is in progress over a scene (QGraphicsSceneDragDropEvent)."
    },
    167: {
        "code": 167,
        "name": "GraphicsSceneDrop",
        "description": "A drag and drop operation is completed over a scene (QGraphicsSceneDragDropEvent)."
    },
    163: {
        "code": 163,
        "name": "GraphicsSceneHelp",
        "description": "The user requests help for a graphics scene (QHelpEvent)."
    },
    160: {
        "code": 160,
        "name": "GraphicsSceneHoverEnter",
        "description": "The mouse cursor enters a hover item in a graphics scene (QGraphicsSceneHoverEvent)."
    },
    162: {
        "code": 162,
        "name": "GraphicsSceneHoverLeave",
        "description": "The mouse cursor leaves a hover item in a graphics scene (QGraphicsSceneHoverEvent)."
    },
    161: {
        "code": 161,
        "name": "GraphicsSceneHoverMove",
        "description": "The mouse cursor moves inside a hover item in a graphics scene (QGraphicsSceneHoverEvent)."
    },
    158: {
        "code": 158,
        "name": "GraphicsSceneMouseDoubleClick",
        "description": "Mouse press again (double click) in a graphics scene (QGraphicsSceneMouseEvent)."
    },
    155: {
        "code": 155,
        "name": "GraphicsSceneMouseMove",
        "description": "Move mouse in a graphics scene (QGraphicsSceneMouseEvent)."
    },
    156: {
        "code": 156,
        "name": "GraphicsSceneMousePress",
        "description": "Mouse press in a graphics scene (QGraphicsSceneMouseEvent)."
    },
    157: {
        "code": 157,
        "name": "GraphicsSceneMouseRelease",
        "description": "Mouse release in a graphics scene (QGraphicsSceneMouseEvent)."
    },
    182: {
        "code": 182,
        "name": "GraphicsSceneMove",
        "description": "Widget was moved (QGraphicsSceneMoveEvent)."
    },
    181: {
        "code": 181,
        "name": "GraphicsSceneResize",
        "description": "Widget was resized (QGraphicsSceneResizeEvent)."
    },
    168: {
        "code": 168,
        "name": "GraphicsSceneWheel",
        "description": "Mouse wheel rolled in a graphics scene (QGraphicsSceneWheelEvent)."
    },
    18: {
        "code": 18,
        "name": "Hide",
        "description": "Widget was hidden (QHideEvent)."
    },
    27: {
        "code": 27,
        "name": "HideToParent",
        "description": "A child widget has been hidden."
    },
    127: {
        "code": 127,
        "name": "HoverEnter",
        "description": "The mouse cursor enters a hover widget (QHoverEvent)."
    },
    128: {
        "code": 128,
        "name": "HoverLeave",
        "description": "The mouse cursor leaves a hover widget (QHoverEvent)."
    },
    129: {
        "code": 129,
        "name": "HoverMove",
        "description": "The mouse cursor moves inside a hover widget (QHoverEvent)."
    },
    96: {
        "code": 96,
        "name": "IconDrag",
        "description": "The main icon of a window has been dragged away (QIconDragEvent)."
    },
    101: {
        "code": 101,
        "name": "IconTextChange",
        "description": "Widget's icon text has been changed. (Deprecated)"
    },
    83: {
        "code": 83,
        "name": "InputMethod",
        "description": "An input method is being used (QInputMethodEvent)."
    },
    207: {
        "code": 207,
        "name": "InputMethodQuery",
        "description": "A input method query event (QInputMethodQueryEvent)"
    },
    169: {
        "code": 169,
        "name": "KeyboardLayoutChange",
        "description": "The keyboard layout has changed."
    },
    6: {
        "code": 6,
        "name": "KeyPress",
        "description": "Key press (QKeyEvent)."
    },
    7: {
        "code": 7,
        "name": "KeyRelease",
        "description": "Key release (QKeyEvent)."
    },
    89: {
        "code": 89,
        "name": "LanguageChange",
        "description": "The application translation changed."
    },
    90: {
        "code": 90,
        "name": "LayoutDirectionChange",
        "description": "The direction of layouts changed."
    },
    76: {
        "code": 76,
        "name": "LayoutRequest",
        "description": "Widget layout needs to be redone."
    },
    11: {
        "code": 11,
        "name": "Leave",
        "description": "Mouse leaves widget's boundaries."
    },
    151: {
        "code": 151,
        "name": "LeaveEditFocus",
        "description": "An editor widget loses focus for editing. QT_KEYPAD_NAVIGATION must be defined."
    },
    125: {
        "code": 125,
        "name": "LeaveWhatsThisMode",
        "description": "Send to toplevel widgets when the application leaves \"What's This?\" mode."
    },
    88: {
        "code": 88,
        "name": "LocaleChange",
        "description": "The system locale has changed."
    },
    176: {
        "code": 176,
        "name": "NonClientAreaMouseButtonDblClick",
        "description": "A mouse double click occurred outside the client area (QMouseEvent)."
    },
    174: {
        "code": 174,
        "name": "NonClientAreaMouseButtonPress",
        "description": "A mouse button press occurred outside the client area (QMouseEvent)."
    },
    175: {
        "code": 175,
        "name": "NonClientAreaMouseButtonRelease",
        "description": "A mouse button release occurred outside the client area (QMouseEvent)."
    },
    173: {
        "code": 173,
        "name": "NonClientAreaMouseMove",
        "description": "A mouse move occurred outside the client area (QMouseEvent)."
    },
    177: {
        "code": 177,
        "name": "MacSizeChange",
        "description": "The user changed his widget sizes (macOS only)."
    },
    43: {
        "code": 43,
        "name": "MetaCall",
        "description": "An asynchronous method invocation via QMetaObject::invokeMethod()."
    },
    102: {
        "code": 102,
        "name": "ModifiedChange",
        "description": "Widgets modification state has been changed."
    },
    4: {
        "code": 4,
        "name": "MouseButtonDblClick",
        "description": "Mouse press again (QMouseEvent)."
    },
    2: {
        "code": 2,
        "name": "MouseButtonPress",
        "description": "Mouse press (QMouseEvent)."
    },
    3: {
        "code": 3,
        "name": "MouseButtonRelease",
        "description": "Mouse release (QMouseEvent)."
    },
    5: {
        "code": 5,
        "name": "MouseMove",
        "description": "Mouse move (QMouseEvent)."
    },
    109: {
        "code": 109,
        "name": "MouseTrackingChange",
        "description": "The mouse tracking state has changed."
    },
    13: {
        "code": 13,
        "name": "Move",
        "description": "Widget's position changed (QMoveEvent)."
    },
    197: {
        "code": 197,
        "name": "NativeGesture",
        "description": "The system has detected a gesture (QNativeGestureEvent)."
    },
    208: {
        "code": 208,
        "name": "OrientationChange",
        "description": "The screens orientation has changes (QScreenOrientationChangeEvent)."
    },
    12: {
        "code": 12,
        "name": "Paint",
        "description": "Screen update necessary (QPaintEvent)."
    },
    39: {
        "code": 39,
        "name": "PaletteChange",
        "description": "Palette of the widget changed."
    },
    131: {
        "code": 131,
        "name": "ParentAboutToChange",
        "description": "The widget parent is about to change."
    },
    21: {
        "code": 21,
        "name": "ParentChange",
        "description": "The widget parent has changed."
    },
    212: {
        "code": 212,
        "name": "PlatformPanel",
        "description": "A platform specific panel has been requested."
    },
    217: {
        "code": 217,
        "name": "PlatformSurface",
        "description": "A native platform surface has been created or is about to be destroyed (QPlatformSurfaceEvent)."
    },
    75: {
        "code": 75,
        "name": "Polish",
        "description": "The widget is polished."
    },
    74: {
        "code": 74,
        "name": "PolishRequest",
        "description": "The widget should be polished."
    },
    123: {
        "code": 123,
        "name": "QueryWhatsThis",
        "description": "The widget should accept the event if it has \"What's This?\" help (QHelpEvent)."
    },
    106: {
        "code": 106,
        "name": "ReadOnlyChange",
        "description": "Widget's read-only state has changed (since Qt 5.4)."
    },
    199: {
        "code": 199,
        "name": "RequestSoftwareInputPanel",
        "description": "A widget wants to open a software input panel (SIP)."
    },
    14: {
        "code": 14,
        "name": "Resize",
        "description": "Widget's size changed (QResizeEvent)."
    },
    204: {
        "code": 204,
        "name": "ScrollPrepare",
        "description": "The object needs to fill in its geometry information (QScrollPrepareEvent)."
    },
    205: {
        "code": 205,
        "name": "Scroll",
        "description": "The object needs to scroll to the supplied position (QScrollEvent)."
    },
    117: {
        "code": 117,
        "name": "Shortcut",
        "description": "Key press in child for shortcut key handling (QShortcutEvent)."
    },
    51: {
        "code": 51,
        "name": "ShortcutOverride",
        "description": "Key press in child, for overriding shortcut key handling (QKeyEvent). When a shortcut is about to trigger, ShortcutOverride is sent to the active window. This allows clients (e.g. widgets) to signal that they will handle the shortcut themselves, by accepting the event. If the shortcut override is accepted, the event is delivered as a normal key press to the focus widget. Otherwise, it triggers the shortcut action, if one exists."
    },
    17: {
        "code": 17,
        "name": "Show",
        "description": "Widget was shown on screen (QShowEvent)."
    },
    26: {
        "code": 26,
        "name": "ShowToParent",
        "description": "A child widget has been shown."
    },
    50: {
        "code": 50,
        "name": "SockAct",
        "description": "Socket activated, used to implement QSocketNotifier."
    },
    192: {
        "code": 192,
        "name": "StateMachineSignal",
        "description": "A signal delivered to a state machine (QStateMachine::SignalEvent)."
    },
    193: {
        "code": 193,
        "name": "StateMachineWrapped",
        "description": "The event is a wrapper for, i.e., contains, another event (QStateMachine::WrappedEvent)."
    },
    112: {
        "code": 112,
        "name": "StatusTip",
        "description": "A status tip is requested (QStatusTipEvent)."
    },
    100: {
        "code": 100,
        "name": "StyleChange",
        "description": "Widget's style has been changed."
    },
    87: {
        "code": 87,
        "name": "TabletMove",
        "description": "Wacom tablet move (QTabletEvent)."
    },
    92: {
        "code": 92,
        "name": "TabletPress",
        "description": "Wacom tablet press (QTabletEvent)."
    },
    93: {
        "code": 93,
        "name": "TabletRelease",
        "description": "Wacom tablet release (QTabletEvent)."
    },
    171: {
        "code": 171,
        "name": "TabletEnterProximity",
        "description": "Wacom tablet enter proximity event (QTabletEvent), sent to QApplication."
    },
    172: {
        "code": 172,
        "name": "TabletLeaveProximity",
        "description": "Wacom tablet leave proximity event (QTabletEvent), sent to QApplication."
    },
    219: {
        "code": 219,
        "name": "TabletTrackingChange",
        "description": "The Wacom tablet tracking state has changed (since Qt 5.9)."
    },
    22: {
        "code": 22,
        "name": "ThreadChange",
        "description": "The object is moved to another thread. This is the last event sent to this object in the previous thread. See QObject::moveToThread()."
    },
    1: {
        "code": 1,
        "name": "Timer",
        "description": "Regular timer events (QTimerEvent)."
    },
    120: {
        "code": 120,
        "name": "ToolBarChange",
        "description": "The toolbar button is toggled on macOS."
    },
    110: {
        "code": 110,
        "name": "ToolTip",
        "description": "A tooltip was requested (QHelpEvent)."
    },
    184: {
        "code": 184,
        "name": "ToolTipChange",
        "description": "The widget's tooltip has changed."
    },
    194: {
        "code": 194,
        "name": "TouchBegin",
        "description": "Beginning of a sequence of touch-screen or track-pad events (QTouchEvent)."
    },
    209: {
        "code": 209,
        "name": "TouchCancel",
        "description": "Cancellation of touch-event sequence (QTouchEvent)."
    },
    196: {
        "code": 196,
        "name": "TouchEnd",
        "description": "End of touch-event sequence (QTouchEvent)."
    },
    195: {
        "code": 195,
        "name": "TouchUpdate",
        "description": "Touch-screen event (QTouchEvent)."
    },
    189: {
        "code": 189,
        "name": "UngrabKeyboard",
        "description": "Item loses keyboard grab (QGraphicsItem only)."
    },
    187: {
        "code": 187,
        "name": "UngrabMouse",
        "description": "Item loses mouse grab (QGraphicsItem, QQuickItem)."
    },
    78: {
        "code": 78,
        "name": "UpdateLater",
        "description": "The widget should be queued to be repainted at a later time."
    },
    77: {
        "code": 77,
        "name": "UpdateRequest",
        "description": "The widget should be repainted."
    },
    111: {
        "code": 111,
        "name": "WhatsThis",
        "description": "The widget should reveal \"What's This?\" help (QHelpEvent)."
    },
    118: {
        "code": 118,
        "name": "WhatsThisClicked",
        "description": "A link in a widget's \"What's This?\" help was clicked."
    },
    31: {
        "code": 31,
        "name": "Wheel",
        "description": "Mouse wheel rolled (QWheelEvent)."
    },
    132: {
        "code": 132,
        "name": "WinEventAct",
        "description": "A Windows-specific activation event has occurred."
    },
    24: {
        "code": 24,
        "name": "WindowActivate",
        "description": "Window was activated."
    },
    103: {
        "code": 103,
        "name": "WindowBlocked",
        "description": "The window is blocked by a modal dialog."
    },
    25: {
        "code": 25,
        "name": "WindowDeactivate",
        "description": "Window was deactivated."
    },
    34: {
        "code": 34,
        "name": "WindowIconChange",
        "description": "The window's icon has changed."
    },
    105: {
        "code": 105,
        "name": "WindowStateChange",
        "description": "The window's state (minimized, maximized or full-screen) has changed (QWindowStateChangeEvent)."
    },
    33: {
        "code": 33,
        "name": "WindowTitleChange",
        "description": "The window title has changed."
    },
    104: {
        "code": 104,
        "name": "WindowUnblocked",
        "description": "The window is unblocked after a modal dialog exited."
    },
    203: {
        "code": 203,
        "name": "WinIdChange",
        "description": "The window system identifer for this native widget has changed."
    },
    126: {
        "code": 126,
        "name": "ZOrderChange",
        "description": "The widget's z-order has changed. This event is never sent to top level windows."
    }
}

class EventObj(object):
    """
    represents qevent
    """
    def __init__(self, event):
        super(EventObj, self).__init__()

        assert(isinstance(event, QEvent))
        self.event = event

        code = event.type()
        if code in CODE_LOOKUP:
            self.data = CODE_LOOKUP[code]
        else:
            self.data = {'code': code, 'name': 'Unknown', 'description': 'Unlisted event code.'}

        self.code = self.data['code']
        self.name = self.data['name']
        self.description = self.data['description']

    def __repr__(self):
        return '{0}: {1} ({2})'.format(type(self.event).__name__, self.name, self.code)

