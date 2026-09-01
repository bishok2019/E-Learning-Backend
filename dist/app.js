const API_BASE = window.location.origin;

const state = {
    token: localStorage.getItem('e_learning_access_token') || '',
    refreshToken: localStorage.getItem('e_learning_refresh_token') || '',
    user: JSON.parse(localStorage.getItem('e_learning_user') || 'null'),
    courses: [],
    enrollments: [],
    currentView: 'overview',
};

const elements = {
    loginForm: document.getElementById('loginForm'),
    registerForm: document.getElementById('registerForm'),
    createCourseForm: document.getElementById('createCourseForm'),
    createUserForm: document.getElementById('createUserForm'),
    enrollmentForm: document.getElementById('enrollmentForm'),
    coursesTableBody: document.getElementById('coursesTableBody'),
    enrollmentsList: document.getElementById('enrollmentsList'),
    authStateBadge: document.getElementById('authStateBadge'),
    logoutBtn: document.getElementById('logoutBtn'),
    loginTriggerBtn: document.getElementById('loginTriggerBtn'),
    unlockLoginBtn: document.getElementById('unlockLoginBtn'),
    authModal: document.getElementById('authModal'),
    closeAuthModalBtn: document.getElementById('closeAuthModalBtn'),
    authLockedState: document.getElementById('authLockedState'),
    adminWorkspace: document.getElementById('adminWorkspace'),
    userProfile: document.getElementById('userProfile'),
    profileName: document.getElementById('profileName'),
    profileEmail: document.getElementById('profileEmail'),
    userInitials: document.getElementById('userInitials'),
    accountUserName: document.getElementById('accountUserName'),
    accountUserEmail: document.getElementById('accountUserEmail'),
    accountUserInitials: document.getElementById('accountUserInitials'),
    accountStatus: document.getElementById('accountStatus'),
    accountTokenStatus: document.getElementById('accountTokenStatus'),
    activeCoursesCount: document.getElementById('activeCoursesCount'),
    enrollmentCount: document.getElementById('enrollmentCount'),
    userCount: document.getElementById('userCount'),
    toast: document.getElementById('toast'),
    navTabs: [...document.querySelectorAll('.nav-tab')],
    authTabs: [...document.querySelectorAll('[data-auth-tab]')],
    viewPanels: [...document.querySelectorAll('[data-view-panel]')],
    addLessonBtn: document.getElementById('addLessonBtn'),
    lessonFieldsContainer: document.getElementById('lessonFieldsContainer'),
    courseDetailModal: document.getElementById('courseDetailModal'),
    closeCourseDetailModalBtn: document.getElementById('closeCourseDetailModalBtn'),
    courseDetailTitle: document.getElementById('courseDetailTitle'),
    courseDetailBody: document.getElementById('courseDetailBody'),
};

function showToast(message, type = 'info') {
    elements.toast.textContent = message;
    elements.toast.classList.remove('hidden');
    elements.toast.style.background =
        type === 'error' ? 'rgba(239, 68, 68, 0.96)' : 'rgba(15, 23, 42, 0.96)';
    clearTimeout(showToast.timer);
    showToast.timer = setTimeout(() => elements.toast.classList.add('hidden'), 2800);
}

function handleApiError(error, fallbackMessage = 'Something went wrong.') {
    const message = error?.detail?.message || error?.detail?.error || error?.detail || fallbackMessage;
    showToast(message, 'error');
    return null;
}

function openAuthModal() {
    elements.authModal.classList.remove('hidden');
}

function closeAuthModal() {
    elements.authModal.classList.add('hidden');
}

function setView(viewName) {
    state.currentView = viewName;

    elements.navTabs.forEach((tab) => {
        tab.classList.toggle('active', tab.dataset.view === viewName);
    });

    elements.viewPanels.forEach((panel) => {
        panel.classList.toggle('active', panel.dataset.viewPanel === viewName);
    });
}

function setAuthState() {
    const isLoggedIn = Boolean(state.token && state.user);

    elements.authLockedState.classList.toggle('hidden', isLoggedIn);
    elements.adminWorkspace.classList.toggle('hidden', !isLoggedIn);
    elements.loginTriggerBtn.classList.toggle('hidden', isLoggedIn);
    elements.logoutBtn.classList.toggle('hidden', !isLoggedIn);
    elements.authStateBadge.textContent = isLoggedIn ? 'Logged in' : 'Guest';
    elements.accountStatus.textContent = isLoggedIn ? 'Active' : 'Guest';
    elements.accountTokenStatus.textContent = isLoggedIn ? 'Present' : 'Not active';

    if (isLoggedIn) {
        const userName = state.user.username || 'Account user';
        const email = state.user.email || 'No email available';
        const initials = (userName || 'U')
            .split(' ')
            .map((part) => part[0])
            .slice(0, 2)
            .join('')
            .toUpperCase();

        elements.profileName.textContent = userName;
        elements.profileEmail.textContent = email;
        elements.userInitials.textContent = initials;
        elements.accountUserName.textContent = userName;
        elements.accountUserEmail.textContent = email;
        elements.accountUserInitials.textContent = initials;
    }
}

async function apiRequest(path, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
    };

    if (state.token) {
        headers.Authorization = `Bearer ${state.token}`;
    }

    const response = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers,
    });

    const payload = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw payload.detail || payload || { detail: 'Request failed' };
    }

    return payload;
}

function saveSession(token, refreshToken, user) {
    state.token = token;
    state.refreshToken = refreshToken;
    state.user = user;

    localStorage.setItem('e_learning_access_token', token);
    localStorage.setItem('e_learning_refresh_token', refreshToken);
    localStorage.setItem('e_learning_user', JSON.stringify(user));

    setAuthState();
    closeAuthModal();
}

function clearSession() {
    state.token = '';
    state.refreshToken = '';
    state.user = null;

    localStorage.removeItem('e_learning_access_token');
    localStorage.removeItem('e_learning_refresh_token');
    localStorage.removeItem('e_learning_user');

    setAuthState();
    showToast('You have been logged out.');
    setView('overview');
}

function createLessonFieldMarkup(index) {
    return `
      <div class="lesson-field-set" data-lesson-index="${index}">
        <div class="lesson-field-set-header">
          <strong>Lesson ${index + 1}</strong>
          <button type="button" class="remove-lesson-btn" data-remove-lesson="${index}">Remove</button>
        </div>
        <label>
          Title
          <input type="text" name="lesson_title_${index}" placeholder="Lesson title" required />
        </label>
        <label>
          Content
          <textarea name="lesson_content_${index}" rows="2" placeholder="Lesson details"></textarea>
        </label>
        <label>
          Order
          <input type="number" name="lesson_order_${index}" value="${index + 1}" min="1" required />
        </label>
      </div>
    `;
}

function renderLessonFields() {
    const lessonCount = 1;
    elements.lessonFieldsContainer.innerHTML = createLessonFieldMarkup(0);
    elements.lessonFieldsContainer.dataset.count = String(lessonCount);
}

function addLessonField() {
    const lessonCount = Number(elements.lessonFieldsContainer.dataset.count || 1);
    const nextIndex = lessonCount;
    elements.lessonFieldsContainer.insertAdjacentHTML('beforeend', createLessonFieldMarkup(nextIndex));
    elements.lessonFieldsContainer.dataset.count = String(nextIndex + 1);
}

function removeLessonField(index) {
    const fieldSet = elements.lessonFieldsContainer.querySelector(`[data-lesson-index="${index}"]`);
    if (fieldSet) fieldSet.remove();

    const allFields = [...elements.lessonFieldsContainer.querySelectorAll('.lesson-field-set')];
    allFields.forEach((field, idx) => {
        field.dataset.lessonIndex = idx;
        const removeBtn = field.querySelector('[data-remove-lesson]');
        if (removeBtn) removeBtn.dataset.removeLesson = idx;
        const titleInput = field.querySelector('input[name^="lesson_title_"]');
        const contentInput = field.querySelector('textarea[name^="lesson_content_"]');
        const orderInput = field.querySelector('input[name^="lesson_order_"]');
        if (titleInput) titleInput.name = `lesson_title_${idx}`;
        if (contentInput) contentInput.name = `lesson_content_${idx}`;
        if (orderInput) orderInput.name = `lesson_order_${idx}`;
    });

    elements.lessonFieldsContainer.dataset.count = String(allFields.length || 1);
}

function renderCourses() {
    if (!state.courses.length) {
        elements.coursesTableBody.innerHTML = '<tr><td colspan="6" class="empty-state">No courses available yet.</td></tr>';
        return;
    }

    elements.coursesTableBody.innerHTML = state.courses
        .map(
            (course, index) => `
        <tr data-course-id="${course.id}" class="course-row" title="Double click to view details">
          <td>${index + 1}</td>
          <td>${course.title || 'Untitled course'}</td>
          <td><span class="status-chip ${String(course.status || 'draft').toLowerCase().replace(/_/g, '_')}">${course.status || 'DRAFT'}</span></td>
          <td>${course.instructor_id ?? '—'}</td>
          <td>${Array.isArray(course.lessons) ? course.lessons.length : 0}</td>
          <td><button class="ghost-button" data-course-id="${course.id}">View</button></td>
        </tr>`
        )
        .join('');

    elements.activeCoursesCount.textContent = state.courses.filter((course) => course.is_active).length;

    elements.coursesTableBody.querySelectorAll('.course-row').forEach((row) => {
        row.addEventListener('dblclick', async () => {
            const courseId = row.dataset.courseId;
            await openCourseDetail(courseId);
        });
    });

    elements.coursesTableBody.querySelectorAll('[data-course-id]').forEach((button) => {
        button.addEventListener('click', async () => {
            const courseId = button.dataset.courseId;
            await openCourseDetail(courseId);
        });
    });
}

function renderEnrollments() {
    if (!state.enrollments.length) {
        elements.enrollmentsList.innerHTML = '<div class="empty-list">No enrollment records yet.</div>';
        return;
    }

    elements.enrollmentsList.innerHTML = state.enrollments
        .map(
            (item) => `
        <div class="enrollment-item">
          <strong>${item.course?.title || 'Course'}</strong>
          <div>Student: ${item.student?.username || item.student_id || 'Unknown'}</div>
          <div class="enrollment-meta">
            <span>Course ID: ${item.course_id || item.course?.id || '—'}</span>
            <span>Student ID: ${item.student_id || item.student?.id || '—'}</span>
            <span>${item.is_completed ? 'Completed' : 'In progress'}</span>
          </div>
        </div>`
        )
        .join('');

    elements.enrollmentCount.textContent = state.enrollments.length;
}

async function openCourseDetail(courseId) {
    try {
        const response = await apiRequest(`/api/v1/courses/retrieve/${courseId}`);
        const fallbackCourse = state.courses.find((course) => String(course.id) === String(courseId)) || {};
        const course = {
            ...fallbackCourse,
            ...(response.data || {}),
        };

        const courseTitle = course.title || fallbackCourse.title || 'Course details';
        const courseLessons = Array.isArray(course.lessons) ? course.lessons : (Array.isArray(fallbackCourse.lessons) ? fallbackCourse.lessons : []);

        elements.courseDetailTitle.textContent = courseTitle;
        elements.courseDetailBody.innerHTML = `
            <div class="course-detail-meta">
                <span>Status: ${course.status || 'DRAFT'}</span>
                <span>Instructor: ${course.instructor_id ?? '—'}</span>
                <span>Active: ${course.is_active ? 'Yes' : 'No'}</span>
            </div>
            <div>
                <strong>Description</strong>
                <p>${course.description || 'No description provided.'}</p>
            </div>
            <div>
                <strong>Lessons</strong>
                <div class="lesson-list">
                    ${courseLessons.length ? courseLessons.map((lesson) => `
                        <div class="lesson-item">
                            <h5>${lesson.title || 'Untitled lesson'}</h5>
                            <p>${lesson.content || 'No lesson content yet.'}</p>
                            <small>Order: ${lesson.order ?? '—'}</small>
                        </div>
                    `).join('') : '<p>No lessons attached yet.</p>'}
                </div>
            </div>
        `;

        elements.courseDetailModal.classList.remove('hidden');
    } catch (error) {
        handleApiError(error, 'Unable to load course details.');
    }
}

async function fetchCourses() {
    try {
        const response = await apiRequest('/api/v1/courses/list?page=1&page_size=50');
        const data = response.data || [];
        state.courses = data;
        renderCourses();
    } catch (error) {
        handleApiError(error, 'Unable to load courses.');
    }
}

async function fetchEnrollments() {
    try {
        const response = await apiRequest('/api/v1/enrollment/list?page=1&page_size=50');
        const data = response.data || [];
        state.enrollments = data;
        renderEnrollments();
    } catch (error) {
        handleApiError(error, 'Unable to load enrollments.');
    }
}

async function fetchUsersCount() {
    if (!state.token) {
        elements.userCount.textContent = '0';
        return;
    }

    try {
        const response = await apiRequest('/api/v1/users/list?page=1&page_size=20');
        const users = response.data || [];
        elements.userCount.textContent = Array.isArray(users) ? users.length : 0;
    } catch (error) {
        handleApiError(error, 'Unable to load users count.');
    }
}

function toggleAuthTab(target) {
    const authTabs = elements.authTabs;
    authTabs.forEach((tab) => tab.classList.toggle('active', tab.dataset.authTab === target));

    document.getElementById('loginForm').classList.toggle('hidden', target !== 'login');
    document.getElementById('registerForm').classList.toggle('hidden', target !== 'register');
}

async function handleLogin(event) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const payload = Object.fromEntries(formData.entries());

    try {
        const response = await apiRequest('/api/v1/auth/login', {
            method: 'POST',
            body: JSON.stringify(payload),
        });

        const data = response.data || {};
        const user = data.user || {};
        saveSession(data.access_token, data.refresh_token, user);
        showToast('Welcome back!');
        event.currentTarget.reset();
        await fetchUsersCount();
        await fetchCourses();
        await fetchEnrollments();
        setView('overview');
    } catch (error) {
        handleApiError(error, 'Login failed.');
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const payload = Object.fromEntries(formData.entries());

    try {
        const response = await apiRequest('/api/v1/auth/register', {
            method: 'POST',
            body: JSON.stringify(payload),
        });

        console.log('[REG] API response received:', response);

        console.log('[REG] Calling showToast...');
        showToast(response.message || 'Registration complete.');

        console.log('[REG] Resetting form...');
        event.currentTarget.reset();

        console.log('[REG] Toggling auth tab to login...');
        toggleAuthTab('login');

        console.log('[REG] Registration success completed');
    } catch (error) {
        console.error('[REG] Registration error caught:', error);
        console.error('[REG] Error stack:', error.stack);
        handleApiError(error, 'Registration failed.');
    }
}

async function handleCreateCourse(event) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const payload = Object.fromEntries(formData.entries());

    payload.instructor_id = Number(formData.get('instructor_id'));
    payload.is_active = formData.get('is_active') === 'on';
    payload.status = payload.status || 'DRAFT';
    payload.lessons = [];

    const lessonFields = [...elements.lessonFieldsContainer.querySelectorAll('.lesson-field-set')];
    lessonFields.forEach((field, index) => {
        const title = field.querySelector(`input[name="lesson_title_${index}"]`)?.value?.trim();
        const content = field.querySelector(`textarea[name="lesson_content_${index}"]`)?.value?.trim();
        const order = field.querySelector(`input[name="lesson_order_${index}"]`)?.value;

        if (title) {
            payload.lessons.push({
                title,
                content: content || '',
                order: Number(order || index + 1),
            });
        }
    });

    try {
        const response = await apiRequest('/api/v1/courses/create', {
            method: 'POST',
            body: JSON.stringify(payload),
        });

        showToast(response.message || 'Course created successfully.');
        event.currentTarget.reset();
        renderLessonFields();
        await fetchCourses();
    } catch (error) {
        handleApiError(error, 'Course creation failed.');
    }
}

async function handleCreateUser(event) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const payload = Object.fromEntries(formData.entries());

    payload.is_active = formData.get('is_active') === 'on';
    payload.is_superuser = false;
    payload.user_type = payload.user_type || 'SYSTEM';

    try {
        const response = await apiRequest('/api/v1/users/create', {
            method: 'POST',
            body: JSON.stringify(payload),
        });

        showToast(response.message || 'User created successfully.');
        event.currentTarget.reset();
        await fetchUsersCount();
    } catch (error) {
        handleApiError(error, 'User creation failed.');
    }
}

async function handleEnrollment(event) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const payload = Object.fromEntries(formData.entries());

    payload.is_completed = formData.get('is_completed') === 'on';

    try {
        const response = await apiRequest('/api/v1/enrollment/create', {
            method: 'POST',
            body: JSON.stringify(payload),
        });

        showToast(response.message || 'Enrollment created successfully.');
        event.currentTarget.reset();
        await fetchEnrollments();
    } catch (error) {
        handleApiError(error, 'Enrollment failed.');
    }
}

function bindGlobalEvents() {
    elements.navTabs.forEach((tab) => {
        tab.addEventListener('click', () => {
            if (!state.token) {
                openAuthModal();
                return;
            }
            setView(tab.dataset.view);
        });
    });

    elements.authTabs.forEach((tab) => {
        tab.addEventListener('click', () => toggleAuthTab(tab.dataset.authTab));
    });

    elements.loginTriggerBtn.addEventListener('click', openAuthModal);
    elements.unlockLoginBtn.addEventListener('click', openAuthModal);
    elements.closeAuthModalBtn.addEventListener('click', closeAuthModal);
    elements.closeCourseDetailModalBtn.addEventListener('click', () => elements.courseDetailModal.classList.add('hidden'));
    elements.loginForm.addEventListener('submit', handleLogin);
    elements.registerForm.addEventListener('submit', handleRegister);
    elements.createCourseForm.addEventListener('submit', handleCreateCourse);
    elements.createUserForm.addEventListener('submit', handleCreateUser);
    elements.enrollmentForm.addEventListener('submit', handleEnrollment);
    elements.logoutBtn.addEventListener('click', clearSession);
    elements.addLessonBtn.addEventListener('click', addLessonField);
    elements.lessonFieldsContainer.addEventListener('click', (event) => {
        const removeBtn = event.target.closest('[data-remove-lesson]');
        if (!removeBtn) return;
        const index = Number(removeBtn.dataset.removeLesson);
        removeLessonField(index);
    });
    document.getElementById('refreshCoursesBtn').addEventListener('click', fetchCourses);
    document.getElementById('refreshEnrollmentsBtn').addEventListener('click', fetchEnrollments);
}

async function initialize() {
    setAuthState();
    setView(state.currentView);
    bindGlobalEvents();
    toggleAuthTab('login');
    renderLessonFields();

    if (state.token && state.user) {
        await fetchCourses();
        await fetchEnrollments();
        await fetchUsersCount();
    }
}

initialize();
