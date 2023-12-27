 
import time
from opcua import Server


def main():
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    uri = "https://opcturkey.com/"
    namespace = server.register_namespace(uri)

    objects = server.get_objects_node()

    object1 = objects.add_object(namespace, "demo_object_for_OPCTURKEY")
    object_variable1 = object1.add_variable(namespace, "demo_object_variable_for_OPCTURKEY", 0.0)
    object_variable1.set_writable()
    
    object2 = objects.add_object(namespace, "demo_object_for_OPCTURKEY_2")
    object_variable2 = object2.add_variable(namespace, "demo_object_variable_for_OPCTURKEY_2", 1.0)
    object_variable2.set_writable()
    
    server.start()

    try:
        count = 0
        while True:
            time.sleep(5)
            if count < 100:
                count += 0.1
            else:
                count=0
            object_variable1.set_value(round(count, 2))

            if count >= 25 and count < 100:
                object_variable2.set_value(count*1.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()

if __name__ == "__main__":
    main()
