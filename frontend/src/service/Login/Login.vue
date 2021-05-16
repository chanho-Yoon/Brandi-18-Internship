<template>
  <div>
    <section class="main">
      <main class="article">
        <h1 class="loginTitle">오늘 사면 내일 도착!</h1>
        <h2 class="subLoginTitle">무료배송으로 내일 받는 브랜디 LOGIN</h2>
        <div class="loginContainer">
          <input
            type="text"
            class="loginInput"
            placeholder="아이디 입력"
            v-model="username"
          />
          <input
            type="password"
            class="loginInput"
            placeholder="비밀번호 입력"
            v-model="password"
          />
          <a class="loginBtn" @click="login">로그인</a>
          <a class="JoinBtn" @click="linkToSignUp">회원가입</a>
          <div class="loginFind">
            <span class="findId">아이디 찾기</span>
            <span class="border" />
            <span class="findPw">비밀번호 찾기</span>
          </div>
          <div></div>
          <h3 class="socialTitle">간편 로그인 / 가입</h3>
          <GoogleLogin
            class="googleLogin"
            :params="params"
            :onSuccess="onSuccess"
          >
            <div class="imgContainer">
              <img src="/Images/google-logo.png" />
            </div>
            Google 계정으로 계속하기
          </GoogleLogin>
        </div>
      </main>
    </section>
  </div>
</template>

<script>
import Message from '@/admin/utils/message'
import { GoogleLogin } from 'vue-google-login'
import API from '@/service/util/service-api'
import { mapMutations } from 'vuex'

const serviceStore = 'serviceStore'

export default {
  components: {
    GoogleLogin
  },
  data() {
    return {
      // 구글 로그인 하기
      params: {
        // client_id: '11' // TODO 실제 키로 변경
        client_id: process.env.VUE_APP_GOOGLE_CLIENT
      },
      renderParams: {
        width: 250,
        height: 50,
        longtitle: true
      },
      username: '',
      password: ''
    }
  },
  methods: {
    ...mapMutations(serviceStore, ['getStorageToken']),
    // 구글 계정 로그인
    onSuccess(googleUser) {
      let res
      const data = {
        id: googleUser.gt.GS,
        email: googleUser.gt.Rt,
        user_type_id: 1, // user_type = 1 (회원)
        social_type_id: 1, // type = 1 (구글)
        social: 'google',
        account_type_id: 3,
        receiving_event_is_agreed: 0,
        notifying_benefit_is_agreed: 0
      }
      const headers = {
        headers: { Authorization: googleUser.qc.id_token }
      }
      API.methods
        // .post(`${SERVER.IP}/user/signin`, data, headers)
        .post('/user/social', data, headers)
        .then((response) => {
          res = response
          console.log(res)
          if (res.data.result.accessToken) {
            localStorage.setItem('access_token', res.data.result.accessToken)
            localStorage.setItem(
              'account_type_id',
              res.data.result.account_type_id
            )
            // this.getStorageToken()
            this.$router.push('/main')
          } else {
            alert('로그인 정보가 맞지 않습니다. 다시 시도해주세요.')
          }
        })
        .catch(() => {
          Message.error(res.data.user_error_message)
        })
    },
    linkToSignUp() {
      if (this.getToken) {
        localStorage.removeItem('access_token')
        this.getStorageToken()
        this.$route.path !== '/main' && this.$router.push('/main')
      } else {
        this.$route.path !== '/signup' && this.$router.push('/signup')
      }
    },
    login() {
      let res
      const data = {
        id: this.username,
        password: this.password,
        social: 'user'
      }
      API.methods
        // .post(`${SERVER.IP}/user/signin`, data)
        .post('/user/signin', data)
        .then((response) => {
          res = response
          localStorage.setItem('access_token', res.data.result.accessToken)
          localStorage.setItem(
            'account_type_id',
            res.data.result.account_type_id
          )
          this.$router.push('/main')
        })
        .catch(() => {
          Message.error(res.data.user_error_message)
          this.username = ''
          this.password = ''
        })
    }
  }
}
</script>

<style lang="scss" scoped>
.main {
  .article {
    max-width: 1300px;
    margin: 200px auto 0;
    display: flex;
    flex-direction: column;
    align-items: center;

    .loginTitle {
      font-size: 34px;
      font-weight: bold;
      color: #ff204b;
      font-family: 'Spoqa Han Sans', Sans-serif;
    }

    .subLoginTitle {
      margin-top: 20px;
      font-size: 32px;
      font-weight: 100;
      font-family: 'Spoqa Han Sans', Sans-serif;
    }

    .loginContainer {
      width: 600px;
      margin-top: 20px;
      display: flex;
      flex-direction: column;
      justify-content: center;

      .loginInput {
        height: 50px;
        border: 1px solid lightgray;
        border-radius: 3px;
        margin-top: 10px;
        padding: 10px;
        outline: none;
        font-size: 14px;
        font-weight: 500;
        color: #333333;
      }

      .loginBtn {
        height: 50px;
        line-height: 50px;
        margin-top: 14px;
        font-size: 13px;
        text-align: center;
        border-radius: 4px;
        background-color: black;
        color: white;
        cursor: pointer;
      }

      .joinBtn {
        height: 50px;
        line-height: 50px;
        margin-top: 4px;
        font-size: 13px;
        text-align: center;
        border: 1px solid black;
        border-radius: 4px;
        cursor: pointer;
      }

      .loginFind {
        text-align: right;
        padding: 17px 0;
        font-size: 13px;
        color: #666;
        border-bottom: 1px solid #ccc;

        .findId,
        .findPw {
          cursor: pointer;
        }

        .border {
          margin: 0 10px;
          border-right: 1px solid #ccc;
        }
      }

      .socialTitle {
        margin: 35px 0 15px;
        text-align: center;
        font-weight: bold;
        font-size: 16px;
      }

      .googleLogin {
        width: 278px;
        height: 50px;
        background-color: white;
        border: 1px solid #bdbdbd;
        border-radius: 5px;
        margin: 0 auto 50px;
        font-weight: 500;
        color: #666;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;

        &:hover {
          color: white;
          background-color: black;
        }

        .imgContainer {
          width: 28px;
          height: 28px;
          margin-right: 10px;

          img {
            width: 100%;
            height: 100%;
          }
        }
      }
    }
  }
}
</style>
