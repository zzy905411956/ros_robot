;; Auto-generated. Do not edit!


(when (boundp 'move_base_msgs::MoveBaseResult)
  (if (not (find-package "MOVE_BASE_MSGS"))
    (make-package "MOVE_BASE_MSGS"))
  (shadow 'MoveBaseResult (find-package "MOVE_BASE_MSGS")))
(unless (find-package "MOVE_BASE_MSGS::MOVEBASERESULT")
  (make-package "MOVE_BASE_MSGS::MOVEBASERESULT"))

(in-package "ROS")
;;//! \htmlinclude MoveBaseResult.msg.html


(defclass move_base_msgs::MoveBaseResult
  :super ros::object
  :slots ())

(defmethod move_base_msgs::MoveBaseResult
  (:init
   (&key
    )
   (send-super :init)
   self)
  (:serialization-length
   ()
   (+
    0
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;;
   self)
  )

(setf (get move_base_msgs::MoveBaseResult :md5sum-) "d41d8cd98f00b204e9800998ecf8427e")
(setf (get move_base_msgs::MoveBaseResult :datatype-) "move_base_msgs/MoveBaseResult")
(setf (get move_base_msgs::MoveBaseResult :definition-)
      "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======

")



(provide :move_base_msgs/MoveBaseResult "d41d8cd98f00b204e9800998ecf8427e")


