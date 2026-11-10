const bieu_mau = document.getElementById("bieu-mau-sinh-vien");
const khung_nhap = document.getElementById("khung-nhap-sinh-vien");
const khung_mon = document.getElementById("danh-sach-mon-nhap");
const mau_mon = document.getElementById("mau-mon-hoc");
const nut_them_mon = document.getElementById("nut-them-mon");
const thong_bao_luu = document.getElementById("thong-bao-luu");

const o_mssv = document.getElementById("mssv-moi");
const o_ho_ten = document.getElementById("ho-ten-moi");

let dang_luu_sinh_vien = false;

const khu_nhap = bieu_mau.closest("details");
const tieu_de_nhap = khu_nhap.querySelector("summary");
const nut_luu_sinh_vien = bieu_mau.querySelector('button[type="submit"]');
const nut_huy_sua = document.getElementById("nut-huy-sua");

let mssv_dang_sua = null;

function cap_nhat_thu_tu_mon() {
    const cac_mon = khung_mon.querySelectorAll(".dong-mon");

    cac_mon.forEach(function (dong_mon, vi_tri) {
        dong_mon.querySelector("legend").textContent =
            `Môn học ${vi_tri + 1}`;

        dong_mon.querySelector(".nut-xoa-mon").disabled =
            cac_mon.length === 1;
    });
}


function them_dong_mon() {
    const dong_mon = mau_mon.content.firstElementChild.cloneNode(true);

    dong_mon.querySelector(".nut-xoa-mon").addEventListener(
        "click",
        function () {
            if (khung_mon.children.length === 1) {
                return;
            }

            dong_mon.remove();
            cap_nhat_thu_tu_mon();
        }
    );

    khung_mon.appendChild(dong_mon);
    cap_nhat_thu_tu_mon();

    return dong_mon;
}


async function luu_sinh_vien(su_kien) {
    su_kien.preventDefault();

    if (dang_luu_sinh_vien) {
        return;
    }

    o_mssv.value = o_mssv.value.trim();
    o_ho_ten.value = o_ho_ten.value.trim();

    const cac_mon = khung_mon.querySelectorAll(".dong-mon");

    for (const dong_mon of cac_mon) {
        const o_ten_mon = dong_mon.querySelector(".ten-mon");
        o_ten_mon.value = o_ten_mon.value.trim();
    }

    if (!bieu_mau.reportValidity()) {
        return;
    }

    const sinh_vien = {
        mssv: o_mssv.value,
        ho_ten: o_ho_ten.value,
        danh_sach_mon: [],
    };

    for (const dong_mon of cac_mon) {
        sinh_vien.danh_sach_mon.push({
            ten_mon: dong_mon.querySelector(".ten-mon").value,
            diem_40: dong_mon.querySelector(".diem-40").valueAsNumber,
            diem_60: dong_mon.querySelector(".diem-60").valueAsNumber,
        });
    }

    dang_luu_sinh_vien = true;
    khung_nhap.disabled = true;

    thong_bao_luu.textContent = "Đang lưu sinh viên...";
    thong_bao_luu.classList.remove("loi");

    try {
        const dang_sua = mssv_dang_sua !== null;
        const url = dang_sua
            ? `/students?${new URLSearchParams({ mssv_cu: mssv_dang_sua })}`
            : "/students";

        const phan_hoi = await fetch(url, {
            method: dang_sua ? "PUT" : "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(sinh_vien),
        });

        const ket_qua = await phan_hoi.json();

        if (!phan_hoi.ok) {
            if (typeof ket_qua.detail === "string") {
                thong_bao_luu.textContent = ket_qua.detail;
            } else {
                thong_bao_luu.textContent =
                    "Dữ liệu chưa hợp lệ. Hãy kiểm tra thông tin và điểm.";
            }

            thong_bao_luu.classList.add("loi");
            return;
        }

        const hanh_dong = dang_sua ? "Đã cập nhật" : "Đã thêm";
        thong_bao_luu.textContent =
            `${hanh_dong} ${ket_qua.ho_ten} (${ket_qua.mssv}). ` +
            `GPA: ${ket_qua.gpa.toFixed(2)}.`;

        dat_lai_bieu_mau();

        document.getElementById("tu-khoa").value = "";
        tai_danh_sach_sinh_vien();
        
    } catch (loi) {
        thong_bao_luu.textContent =
            "Không lưu được dữ liệu. Hãy kiểm tra kết nối và thử lại.";

        thong_bao_luu.classList.add("loi");
        console.error(loi);
    } finally {
        khung_nhap.disabled = false;
        dang_luu_sinh_vien = false;
    }
}

function chon_che_do_bieu_mau(mssv_cu) {
    mssv_dang_sua = mssv_cu;
    const dang_sua = mssv_cu !== null;
    const tieu_de = dang_sua ? "Chỉnh sửa sinh viên" : "Thêm sinh viên";

    tieu_de_nhap.textContent = tieu_de;
    bieu_mau.setAttribute("aria-label", tieu_de);
    nut_luu_sinh_vien.textContent = dang_sua ? "Lưu thay đổi" : "Lưu sinh viên";
    nut_huy_sua.hidden = !dang_sua;
}

function dat_lai_bieu_mau() {
    chon_che_do_bieu_mau(null);
    bieu_mau.reset();
    khung_mon.replaceChildren();
    them_dong_mon();
}

function mo_bieu_mau_chinh_sua(sinh_vien) {
    if (dang_luu_sinh_vien) {
        return;
    }

    chon_che_do_bieu_mau(sinh_vien.mssv);
    o_mssv.value = sinh_vien.mssv;
    o_ho_ten.value = sinh_vien.ho_ten;
    khung_mon.replaceChildren();

    for (const mon of sinh_vien.danh_sach_mon) {
        const dong_mon = them_dong_mon();
        dong_mon.querySelector(".ten-mon").value = mon.ten_mon;
        dong_mon.querySelector(".diem-40").value = mon.diem_40;
        dong_mon.querySelector(".diem-60").value = mon.diem_60;
    }

    thong_bao_luu.textContent = "";
    thong_bao_luu.classList.remove("loi");
    khu_nhap.open = true;
    o_mssv.focus();
}

nut_huy_sua.addEventListener("click", function () {
    dat_lai_bieu_mau();
    thong_bao_luu.textContent = "";
    thong_bao_luu.classList.remove("loi");
    o_mssv.focus();
});


nut_them_mon.addEventListener("click", them_dong_mon);
bieu_mau.addEventListener("submit", luu_sinh_vien);

them_dong_mon();