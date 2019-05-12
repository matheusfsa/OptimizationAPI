#define PY_SSIZE_T_CLEAN
#include <Python.h>

// Function 1: A simple 'hello world' function
static PyObject* helloworld(PyObject* self, PyObject* args)
{
    printf("Hello World\n");
    return Py_None;
}
int _asdf(double pr[], int length) {
    for (int index = 0; index < length; index++)
        printf("pr[%d] = %f\n", index, pr[index]);
    return 0;
}
static PyObject*	dominance(PyObject* self, PyObject* args)
{
    PyObject *float_list1;
    PyObject *float_list2;
    int pr_length,pr2_length;
    double *pr,*pr2;
    int best_is_one = 0;
    int best_is_two = 0;
    if (!PyArg_ParseTuple(args, "OO", &float_list1,&float_list2))
        return NULL;
    pr_length = PyObject_Length(float_list1);
    pr2_length = PyObject_Length(float_list2);
    if (pr_length < 0 || pr2_length < 0)
        return NULL;	

    pr = (double *) malloc(sizeof(double *) * pr_length);
    pr2 = (double *) malloc(sizeof(double *) * pr2_length);
    if (pr == NULL)
        return NULL;
    for (int index = 0; index < pr_length; index++) {
        PyObject *item, *item2;
        item = PyList_GetItem(float_list1, index);
	item2 = PyList_GetItem(float_list2, index);
        if (!PyFloat_Check(item))
            pr[index] = 0.0;
        if (!PyFloat_Check(item2))
            pr2[index] = 0.0   ;
        pr[index] = PyFloat_AsDouble(item);
        pr2[index] = PyFloat_AsDouble(item2);
        if(pr[index] < pr2[index]){
		best_is_one = 1;        
	}else if(pr[index] > pr2[index]){
		best_is_two = 1;
	}
    }
    if(best_is_one > best_is_two){
        return PyLong_FromLong(1);	
    }
    if(best_is_one < best_is_two){
       return PyLong_FromLong(-1);	
    }
    return PyLong_FromLong(0);		
}

// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition
static PyMethodDef myMethods[] = {
    { "helloworld", helloworld, METH_NOARGS, "Prints Hello World" },
    { "dominance", dominance, METH_VARARGS, "Calcula dom" },
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef domModule = {
    PyModuleDef_HEAD_INIT,
    "myModule",
    "Test Module",
    -1,
    myMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_domModule(void)
{
    return PyModule_Create(&domModule);
}

