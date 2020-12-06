
import sys
sys.path.insert(0, '../tensorflow/')
import tensorflow as tf

from tensorflow.python.ops.linalg.sparse import sparse_csr_matrix_ops
#from tensorflow.raw_ops import CSRSparseMatrixToSparseTensor

def sparse_tensor_mul(a_st, b_st):
    a_sm = sparse_csr_matrix_ops.sparse_tensor_to_csr_sparse_matrix(
        a_st.indices, a_st.values, a_st.dense_shape)
    b_sm = sparse_csr_matrix_ops.sparse_tensor_to_csr_sparse_matrix(
        b_st.indices, b_st.values, b_st.dense_shape)

    print(a_sm)

    # Compute the CSR SparseMatrix matrix multiplication
    c_sm = sparse_csr_matrix_ops.sparse_matrix_sparse_mat_mul(
        a=a_sm, b=b_sm, type=tf.float32)

    c_st = tf.SparseTensor(*sparse_csr_matrix_ops.CSRSparseMatrixToSparseTensor(c_sm, tf.bool))
    return c_st


a = tf.SparseTensor([[0,0,0], [2, 3, 2]], [1.0, 1.0], [5, 6, 4])
# print(a.values)
b = tf.SparseTensor([[2, 0, 2]], [1.0,], [5, 6, 4])

#c = sparse_tensor_mul(a,I b)
print(c)



