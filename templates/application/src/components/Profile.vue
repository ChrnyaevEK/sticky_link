<template id="profile">
    <div class="pt-3">
        <div class="form-group">
            <label>User name</label>
            <p class="form-control">{{ Shared.user.username }}</p>
        </div>
        <div class="form-group">
            <label>E-mail</label>
            <p class="form-control">{{ Shared.user.email }}</p>
        </div>
        <div class="form-group" v-if="Shared.user.first_name">
            <label>First name</label>
            <p class="form-control">{{ Shared.user.first_name }}</p>
        </div>
        <div class="form-group" v-if="Shared.user.last_name">
            <label>Last name</label>
            <p class="form-control">{{ Shared.user.last_name }}</p>
        </div>
        <hr />
        <div class="d-flex justify-content-end">
            <a href="{% url 'logout' %}" class="px-3">Log out</a>
            <a href="{% url 'password_change' %}" class="px-3">Change password</a>
        </div>
    </div>
</template>

<script>
import { Shared } from "../common.js";
export default {
    name: 'Profile',
    template: '#profile',
    data(){
        return {
            Shared
        }
    }
}
</script>
