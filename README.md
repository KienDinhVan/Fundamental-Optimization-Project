# Fundamental of optimization project

### Problem: TimeTable assign slot and room to classes

#### Description:

Có N lớp 1,2,..., N cần được xếp thời khóa biểu. Mỗi lớp i có t(i) là số  tiết và g(i) là giáo viên đã được phân công dạy lớp đó và s(i) là số sinh  viên của lớp. Có M phòng học 1, 2, ..., M, trong đó c(i) là số chỗ ngồi của phòng i. Trong tuần có 5 ngày (từ thứ 2 đến thứ 5), mỗi ngày chia thành 12 tiết (6  tiết sáng và 6 tiết chiều).  Các tiết của các ngày được đánh số lần lượt từ 1 đến 60.

Hãy lập thời khóa biểu (xác định ngày, tiết và phòng gán cho mỗi lớp):

-Hai lớp có chung giáo viên thì phải xếp thời khóa biểu tách rời nhau 

-Số sinh viên trong mỗi lớp phải nhỏ hơn hoặc bằng số chỗ ngồi của phòng học

-Số lớp được xếp thời khóa biểu là lớn nhất

#### Input:

Line 1: ghi N và M (1 <= N <= 1000, 1 <= M <= 100)

Line i+1 (i = 1,…, N): ghi t(i), g(i) và s(i)  (1 <= t(i) <= 4, 1 <= g(i) <= 100, 1 <= s(i) <= 200)

Line N+2: ghi c(1), c(2), …, c(M) (1 <= c(i) <= 300)

#### Output:

Line 1: contains a positive integer Q

Line q + 1 (q = 1, 2, . . ., Q): contains 3 positive integers i, u, and v in which class i is assigned to slot u and room u
