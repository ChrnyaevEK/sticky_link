import Rollbar from "vue-rollbar";
import Vue from "vue";

Vue.use(Rollbar, {
    enabled: process.env.NODE_ENV === "production",
    accessToken: "352f084b3c4b4a60951b25ce2252fb6f",
    captureUncaught: process.env.NODE_ENV === "production",
    captureUnhandledRejections: process.env.NODE_ENV === "production",
    payload: {
        environment: "production",
    },
})

export default Vue.rollbar