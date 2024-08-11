function get_code(e) {
    // const jsdom = require("jsdom");
    // const { JSDOM } = jsdom;
    // const dom = new JSDOM('<html><head></head><body>js</body></html>');
    // window = dom.window;
    // document = window.document;
    // window.d_key = "wijrKSCUiQuGbrwsgyEMyIx7Uogmfe85";
    // window.d_iv = "ho6KJIIz9WV7nozZl5fVnG7MtDUcSUB1";
    var n, r, o = o || function (e, t) {
        var n = {}
            , r = n.lib = {}
            , o = r.Base = function () {
                function e() { }
                return {
                    extend: function (t) {
                        e.prototype = this;
                        var n = new e;
                        return t && n.mixIn(t),
                            n.$super = this,
                            n
                    },
                    create: function () {
                        var e = this.extend();
                        return e.init.apply(e, arguments),
                            e
                    },
                    init: function () { },
                    mixIn: function (e) {
                        for (var t in e)
                            e.hasOwnProperty(t) && (this[t] = e[t]);
                        e.hasOwnProperty("toString") && (this.toString = e.toString)
                    },
                    clone: function () {
                        return this.$super.extend(this)
                    }
                }
            }()
            , i = r.WordArray = o.extend({
                init: function (e, t) {
                    e = this.words = e || [],
                        this.sigBytes = void 0 != t ? t : 4 * e.length
                },
                toString: function (e) {
                    return (e || s).stringify(this)
                },
                concat: function (e) {
                    var t = this.words
                        , n = e.words
                        , r = this.sigBytes;
                    e = e.sigBytes;
                    if (this.clamp(),
                        r % 4)
                        for (var o = 0; o < e; o++)
                            t[r + o >>> 2] |= (n[o >>> 2] >>> 24 - o % 4 * 8 & 255) << 24 - (r + o) % 4 * 8;
                    else if (65535 < n.length)
                        for (o = 0; o < e; o += 4)
                            t[r + o >>> 2] = n[o >>> 2];
                    else
                        t.push.apply(t, n);
                    return this.sigBytes += e,
                        this
                },
                clamp: function () {
                    var t = this.words
                        , n = this.sigBytes;
                    t[n >>> 2] &= 4294967295 << 32 - n % 4 * 8,
                        t.length = e.ceil(n / 4)
                },
                clone: function () {
                    var e = o.clone.call(this);
                    return e.words = this.words.slice(0),
                        e
                },
                random: function (t) {
                    for (var n = [], r = 0; r < t; r += 4)
                        n.push(4294967296 * e.random() | 0);
                    return i.create(n, t)
                }
            })
            , a = n.enc = {}
            , s = a.Hex = {
                stringify: function (e) {
                    for (var t = e.words, n = (e = e.sigBytes,
                        []), r = 0; r < e; r++) {
                        var o = t[r >>> 2] >>> 24 - r % 4 * 8 & 255;
                        n.push((o >>> 4).toString(16)),
                            n.push((15 & o).toString(16))
                    }
                    return n.join("")
                },
                parse: function (e) {
                    for (var t = e.length, n = [], r = 0; r < t; r += 2)
                        n[r >>> 3] |= parseInt(e.substr(r, 2), 16) << 24 - r % 8 * 4;
                    return i.create(n, t / 2)
                }
            }
            , c = a.Latin1 = {
                stringify: function (e) {
                    for (var t = e.words, n = (e = e.sigBytes,
                        []), r = 0; r < e; r++)
                        n.push(String.fromCharCode(t[r >>> 2] >>> 24 - r % 4 * 8 & 255));
                    return n.join("")
                },
                parse: function (e) {
                    for (var t = e.length, n = [], r = 0; r < t; r++)
                        n[r >>> 2] |= (255 & e.charCodeAt(r)) << 24 - r % 4 * 8;
                    return i.create(n, t)
                }
            }
            , l = a.Utf8 = {
                stringify: function (e) {
                    try {
                        return decodeURIComponent(escape(c.stringify(e)))
                    } catch (e) {
                        throw Error("Malformed UTF-8 data")
                    }
                },
                parse: function (e) {
                    return c.parse(unescape(encodeURIComponent(e)))
                }
            }
            , u = r.BufferedBlockAlgorithm = o.extend({
                reset: function () {
                    this._data = i.create(),
                        this._nDataBytes = 0
                },
                _append: function (e) {
                    "string" == typeof e && (e = l.parse(e)),
                        this._data.concat(e),
                        this._nDataBytes += e.sigBytes
                },
                _process: function (t) {
                    var n = this._data
                        , r = n.words
                        , o = n.sigBytes
                        , a = this.blockSize
                        , s = o / (4 * a);
                    t = (s = t ? e.ceil(s) : e.max((0 | s) - this._minBufferSize, 0)) * a,
                        o = e.min(4 * t, o);
                    if (t) {
                        for (var c = 0; c < t; c += a)
                            this._doProcessBlock(r, c);
                        c = r.splice(0, t),
                            n.sigBytes -= o
                    }
                    return i.create(c, o)
                },
                clone: function () {
                    var e = o.clone.call(this);
                    return e._data = this._data.clone(),
                        e
                },
                _minBufferSize: 0
            });
        r.Hasher = u.extend({
            init: function () {
                this.reset()
            },
            reset: function () {
                u.reset.call(this),
                    this._doReset()
            },
            update: function (e) {
                return this._append(e),
                    this._process(),
                    this
            },
            finalize: function (e) {
                return e && this._append(e),
                    this._doFinalize(),
                    this._hash
            },
            clone: function () {
                var e = u.clone.call(this);
                return e._hash = this._hash.clone(),
                    e
            },
            blockSize: 16,
            _createHelper: function (e) {
                return function (t, n) {
                    return e.create(n).finalize(t)
                }
            },
            _createHmacHelper: function (e) {
                return function (t, n) {
                    return d.HMAC.create(e, n).finalize(t)
                }
            }
        });
        var d = n.algo = {};
        return n
    }(Math);
    r = (n = o).lib.WordArray,
        n.enc.Base64 = {
            stringify: function (e) {
                var t = e.words
                    , n = e.sigBytes
                    , r = this._map;
                e.clamp(),
                    e = [];
                for (var o = 0; o < n; o += 3)
                    for (var i = (t[o >>> 2] >>> 24 - o % 4 * 8 & 255) << 16 | (t[o + 1 >>> 2] >>> 24 - (o + 1) % 4 * 8 & 255) << 8 | t[o + 2 >>> 2] >>> 24 - (o + 2) % 4 * 8 & 255, a = 0; 4 > a && o + .75 * a < n; a++)
                        e.push(r.charAt(i >>> 6 * (3 - a) & 63));
                if (t = r.charAt(64))
                    for (; e.length % 4;)
                        e.push(t);
                return e.join("")
            },
            parse: function (e) {
                var t = (e = e.replace(/\s/g, "")).length
                    , n = this._map;
                (o = n.charAt(64)) && -1 != (o = e.indexOf(o)) && (t = o);
                for (var o = [], i = 0, a = 0; a < t; a++)
                    if (a % 4) {
                        var s = n.indexOf(e.charAt(a - 1)) << a % 4 * 2
                            , c = n.indexOf(e.charAt(a)) >>> 6 - a % 4 * 2;
                        o[i >>> 2] |= (s | c) << 24 - i % 4 * 8,
                            i++
                    }
                return r.create(o, i)
            },
            _map: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        },
        function (e) {
            function t(e, t, n, r, o, i, a) {
                return ((e = e + (t & n | ~t & r) + o + a) << i | e >>> 32 - i) + t
            }
            function n(e, t, n, r, o, i, a) {
                return ((e = e + (t & r | n & ~r) + o + a) << i | e >>> 32 - i) + t
            }
            function r(e, t, n, r, o, i, a) {
                return ((e = e + (t ^ n ^ r) + o + a) << i | e >>> 32 - i) + t
            }
            function i(e, t, n, r, o, i, a) {
                return ((e = e + (n ^ (t | ~r)) + o + a) << i | e >>> 32 - i) + t
            }
            var a = o
                , s = (c = a.lib).WordArray
                , c = c.Hasher
                , l = a.algo
                , u = [];
            !function () {
                for (var t = 0; 64 > t; t++)
                    u[t] = 4294967296 * e.abs(e.sin(t + 1)) | 0
            }(),
                l = l.M = c.extend({
                    _doReset: function () {
                        this._hash = s.create([1732584193, 4023233417, 2562383102, 271733878])
                    },
                    _doProcessBlock: function (e, o) {
                        for (var a = 0; 16 > a; a++) {
                            var s = e[c = o + a];
                            e[c] = 16711935 & (s << 8 | s >>> 24) | 4278255360 & (s << 24 | s >>> 8)
                        }
                        s = (c = this._hash.words)[0];
                        var c, l = c[1], d = c[2], f = c[3];
                        for (a = 0; 64 > a; a += 4)
                            16 > a ? l = t(l, d = t(d, f = t(f, s = t(s, l, d, f, e[o + a], 7, u[a]), l, d, e[o + a + 1], 12, u[a + 1]), s, l, e[o + a + 2], 17, u[a + 2]), f, s, e[o + a + 3], 22, u[a + 3]) : 32 > a ? l = n(l, d = n(d, f = n(f, s = n(s, l, d, f, e[o + (a + 1) % 16], 5, u[a]), l, d, e[o + (a + 6) % 16], 9, u[a + 1]), s, l, e[o + (a + 11) % 16], 14, u[a + 2]), f, s, e[o + a % 16], 20, u[a + 3]) : 48 > a ? l = r(l, d = r(d, f = r(f, s = r(s, l, d, f, e[o + (3 * a + 5) % 16], 4, u[a]), l, d, e[o + (3 * a + 8) % 16], 11, u[a + 1]), s, l, e[o + (3 * a + 11) % 16], 16, u[a + 2]), f, s, e[o + (3 * a + 14) % 16], 23, u[a + 3]) : l = i(l, d = i(d, f = i(f, s = i(s, l, d, f, e[o + 3 * a % 16], 6, u[a]), l, d, e[o + (3 * a + 7) % 16], 10, u[a + 1]), s, l, e[o + (3 * a + 14) % 16], 15, u[a + 2]), f, s, e[o + (3 * a + 5) % 16], 21, u[a + 3]);
                        c[0] = c[0] + s | 0,
                            c[1] = c[1] + l | 0,
                            c[2] = c[2] + d | 0,
                            c[3] = c[3] + f | 0
                    },
                    _doFinalize: function () {
                        var e = this._data
                            , t = e.words
                            , n = 8 * this._nDataBytes
                            , r = 8 * e.sigBytes;
                        for (t[r >>> 5] |= 128 << 24 - r % 32,
                            t[14 + (r + 64 >>> 9 << 4)] = 16711935 & (n << 8 | n >>> 24) | 4278255360 & (n << 24 | n >>> 8),
                            e.sigBytes = 4 * (t.length + 1),
                            this._process(),
                            e = this._hash.words,
                            t = 0; 4 > t; t++)
                            n = e[t],
                                e[t] = 16711935 & (n << 8 | n >>> 24) | 4278255360 & (n << 24 | n >>> 8)
                    }
                }),
                a.M = c._createHelper(l),
                a.HmacMD5 = c._createHmacHelper(l)
        }(Math),
        function () {
            var e, t = o, n = (e = t.lib).Base, r = e.WordArray, i = (e = t.algo).EvpKDF = n.extend({
                cfg: n.extend({
                    keySize: 4,
                    hasher: e.MD5,
                    iterations: 1
                }),
                init: function (e) {
                    this.cfg = this.cfg.extend(e)
                },
                compute: function (e, t) {
                    for (var n = (s = this.cfg).hasher.create(), o = r.create(), i = o.words, a = s.keySize, s = s.iterations; i.length < a;) {
                        c && n.update(c);
                        var c = n.update(e).finalize(t);
                        n.reset();
                        for (var l = 1; l < s; l++)
                            c = n.finalize(c),
                                n.reset();
                        o.concat(c)
                    }
                    return o.sigBytes = 4 * a,
                        o
                }
            });
            t.EvpKDF = function (e, t, n) {
                return i.create(n).compute(e, t)
            }
        }();
    var i = o.M("getUtilsFromFile")
        , a = o.enc.Utf8.parse(i);
    o.lib.Cipher || function (e) {
        var t = (h = o).lib
            , n = t.Base
            , r = t.WordArray
            , i = t.BufferedBlockAlgorithm
            , a = h.enc.Base64
            , s = h.algo.EvpKDF
            , c = t.Cipher = i.extend({
                cfg: n.extend(),
                createEncryptor: function (e, t) {
                    return this.create(this._ENC_XFORM_MODE, e, t)
                },
                createDecryptor: function (e, t) {
                    return this.create(this._DEC_XFORM_MODE, e, t)
                },
                init: function (e, t, n) {
                    this.cfg = this.cfg.extend(n),
                        this._xformMode = e,
                        this._key = t,
                        this.reset()
                },
                reset: function () {
                    i.reset.call(this),
                        this._doReset()
                },
                process: function (e) {
                    return this._append(e),
                        this._process()
                },
                finalize: function (e) {
                    return e && this._append(e),
                        this._doFinalize()
                },
                keySize: 4,
                ivSize: 4,
                _ENC_XFORM_MODE: 1,
                _DEC_XFORM_MODE: 2,
                _createHelper: function (e) {
                    return {
                        e: function (t, n, r) {
                            return ("string" == typeof n ? m : p).encrypt(e, t, n, r)
                        },
                        d: function (t, n, r) {
                            return ("string" == typeof n ? m : p).d(e, t, n, r)
                        }
                    }
                }
            });
        t.StreamCipher = c.extend({
            _doFinalize: function () {
                return this._process(!0)
            },
            blockSize: 1
        });
        var l = h.mode = {}
            , u = t.BlockCipherMode = n.extend({
                createEncryptor: function (e, t) {
                    return this.Encryptor.create(e, t)
                },
                createDecryptor: function (e, t) {
                    return this.Decryptor.create(e, t)
                },
                init: function (e, t) {
                    this._cipher = e,
                        this._iv = t
                }
            })
            , d = (l = l.CBC = function () {
                function t(t, n, r) {
                    var o = this._iv;
                    o ? this._iv = e : o = this._prevBlock;
                    for (var i = 0; i < r; i++)
                        t[n + i] ^= o[i]
                }
                var n = u.extend();
                return n.Encryptor = n.extend({
                    processBlock: function (e, n) {
                        var r = this._cipher
                            , o = r.blockSize;
                        t.call(this, e, n, o),
                            r.encryptBlock(e, n),
                            this._prevBlock = e.slice(n, n + o)
                    }
                }),
                    n.Decryptor = n.extend({
                        processBlock: function (e, n) {
                            var r = this._cipher
                                , o = r.blockSize
                                , i = e.slice(n, n + o);
                            r.decryptBlock(e, n),
                                t.call(this, e, n, o),
                                this._prevBlock = i
                        }
                    }),
                    n
            }(),
                (h.pad = {}).Pkcs7 = {
                    pad: function (e, t) {
                        for (var n, o = (n = (n = 4 * t) - e.sigBytes % n) << 24 | n << 16 | n << 8 | n, i = [], a = 0; a < n; a += 4)
                            i.push(o);
                        n = r.create(i, n),
                            e.concat(n)
                    },
                    unpad: function (e) {
                        e.sigBytes -= 255 & e.words[e.sigBytes - 1 >>> 2]
                    }
                });
        t.BlockCipher = c.extend({
            cfg: c.cfg.extend({
                mode: l,
                padding: d
            }),
            reset: function () {
                c.reset.call(this);
                var e = (t = this.cfg).iv
                    , t = t.mode;
                if (this._xformMode == this._ENC_XFORM_MODE)
                    var n = t.createEncryptor;
                else
                    n = t.createDecryptor,
                        this._minBufferSize = 1;
                this._mode = n.call(t, this, e && e.words)
            },
            _doProcessBlock: function (e, t) {
                this._mode.processBlock(e, t)
            },
            _doFinalize: function () {
                var e = this.cfg.padding;
                if (this._xformMode == this._ENC_XFORM_MODE) {
                    e.pad(this._data, this.blockSize);
                    var t = this._process(!0)
                } else
                    t = this._process(!0),
                        e.unpad(t);
                return t
            },
            blockSize: 4
        });
        var f = t.CipherParams = n.extend({
            init: function (e) {
                this.mixIn(e)
            },
            toString: function (e) {
                return (e || this.formatter).stringify(this)
            }
        })
            , p = (l = (h.format = {}).OpenSSL = {
                stringify: function (e) {
                    var t = e.ciphertext;
                    return (t = ((e = e.salt) ? r.create([1398893684, 1701076831]).concat(e).concat(t) : t).toString(a)).replace(/(.{64})/g, "$1\n")
                },
                parse: function (e) {
                    var t = (e = a.parse(e)).words;
                    if (1398893684 == t[0] && 1701076831 == t[1]) {
                        var n = r.create(t.slice(2, 4));
                        t.splice(0, 4),
                            e.sigBytes -= 16
                    }
                    return f.create({
                        ciphertext: e,
                        salt: n
                    })
                }
            },
                t.SerializableCipher = n.extend({
                    cfg: n.extend({
                        format: l
                    }),
                    e: function (e, t, n, r) {
                        r = this.cfg.extend(r),
                            t = (o = e.createEncryptor(n, r)).finalize(t);
                        var o = o.cfg;
                        return f.create({
                            ciphertext: t,
                            key: n,
                            iv: o.iv,
                            algorithm: e,
                            mode: o.mode,
                            padding: o.padding,
                            blockSize: e.blockSize,
                            formatter: r.format
                        })
                    },
                    d: function (e, t, n, r) {
                        return r = this.cfg.extend(r),
                            t = this._parse(t, r.format),
                            e.createDecryptor(n, r).finalize(t.ciphertext)
                    },
                    _parse: function (e, t) {
                        return "string" == typeof e ? t.parse(e) : e
                    }
                }))
            , h = (h.kdf = {}).OpenSSL = {
                compute: function (e, t, n, o) {
                    return o || (o = r.random(8)),
                        e = s.create({
                            keySize: t + n
                        }).compute(e, o),
                        n = r.create(e.words.slice(t), 4 * n),
                        e.sigBytes = 4 * t,
                        f.create({
                            key: e,
                            iv: n,
                            salt: o
                        })
                }
            }
            , m = t.PasswordBasedCipher = p.extend({
                cfg: p.cfg.extend({
                    kdf: h
                }),
                e: function (e, t, n, r) {
                    return n = (r = this.cfg.extend(r)).kdf.compute(n, e.keySize, e.ivSize),
                        r.iv = n.iv,
                        (e = p.encrypt.call(this, e, t, n.key, r)).mixIn(n),
                        e
                },
                d: function (e, t, n, r) {
                    return r = this.cfg.extend(r),
                        t = this._parse(t, r.format),
                        n = r.kdf.compute(n, e.keySize, e.ivSize, t.salt),
                        r.iv = n.iv,
                        p.decrypt.call(this, e, t, n.key, r)
                }
            })
    }();
    var s = o.enc.Utf8.parse("getClassFromFile");
    !function () {
        var e = o
            , t = e.lib.BlockCipher
            , n = e.algo
            , r = []
            , i = []
            , a = []
            , s = []
            , c = []
            , l = []
            , u = []
            , d = []
            , f = []
            , p = [];
        !function () {
            for (var e = [], t = 0; 256 > t; t++)
                e[t] = 128 > t ? t << 1 : t << 1 ^ 283;
            var n = 0
                , o = 0;
            for (t = 0; 256 > t; t++) {
                var h = (h = o ^ o << 1 ^ o << 2 ^ o << 3 ^ o << 4) >>> 8 ^ 255 & h ^ 99;
                r[n] = h,
                    i[h] = n;
                var m = e[n]
                    , g = e[m]
                    , v = e[g]
                    , y = 257 * e[h] ^ 16843008 * h;
                a[n] = y << 24 | y >>> 8,
                    s[n] = y << 16 | y >>> 16,
                    c[n] = y << 8 | y >>> 24,
                    l[n] = y,
                    y = 16843009 * v ^ 65537 * g ^ 257 * m ^ 16843008 * n,
                    u[h] = y << 24 | y >>> 8,
                    d[h] = y << 16 | y >>> 16,
                    f[h] = y << 8 | y >>> 24,
                    p[h] = y,
                    n ? (n = m ^ e[e[e[v ^ m]]],
                        o ^= e[e[o]]) : n = o = 1
            }
        }(),
            // window.Crypto = null,
            o.mode.ECB = o.mode.CBC,
            o.pad.ZERO = o.pad.Pkcs7;
        var h = [0, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54];
        n = n.AlocalStorage = t.extend({
            _doReset: function () {
                for (var e = (n = this._key).words, t = n.sigBytes / 4, n = 4 * ((this._nRounds = t + 6) + 1), o = this._keySchedule = [], i = 0; i < n; i++)
                    if (i < t)
                        o[i] = e[i];
                    else {
                        var a = o[i - 1];
                        i % t ? 6 < t && 4 == i % t && (a = r[a >>> 24] << 24 | r[a >>> 16 & 255] << 16 | r[a >>> 8 & 255] << 8 | r[255 & a]) : (a = r[(a = a << 8 | a >>> 24) >>> 24] << 24 | r[a >>> 16 & 255] << 16 | r[a >>> 8 & 255] << 8 | r[255 & a],
                            a ^= h[i / t | 0] << 24),
                            o[i] = o[i - t] ^ a
                    }
                for (e = this._invKeySchedule = [],
                    t = 0; t < n; t++)
                    i = n - t,
                        a = t % 4 ? o[i] : o[i - 4],
                        e[t] = 4 > t || 4 >= i ? a : u[r[a >>> 24]] ^ d[r[a >>> 16 & 255]] ^ f[r[a >>> 8 & 255]] ^ p[r[255 & a]]
            },
            encryptBlock: function (e, t) {
                this._doCryptBlock(e, t, this._keySchedule, a, s, c, l, r)
            },
            decryptBlock: function (e, t) {
                var n = e[t + 1];
                e[t + 1] = e[t + 3],
                    e[t + 3] = n,
                    this._doCryptBlock(e, t, this._invKeySchedule, u, d, f, p, i),
                    n = e[t + 1],
                    e[t + 1] = e[t + 3],
                    e[t + 3] = n
            },
            _doCryptBlock: function (e, t, n, r, o, i, a, s) {
                for (var c = this._nRounds, l = e[t] ^ n[0], u = e[t + 1] ^ n[1], d = e[t + 2] ^ n[2], f = e[t + 3] ^ n[3], p = 4, h = 1; h < c; h++) {
                    var m = r[l >>> 24] ^ o[u >>> 16 & 255] ^ i[d >>> 8 & 255] ^ a[255 & f] ^ n[p++]
                        , g = r[u >>> 24] ^ o[d >>> 16 & 255] ^ i[f >>> 8 & 255] ^ a[255 & l] ^ n[p++]
                        , v = r[d >>> 24] ^ o[f >>> 16 & 255] ^ i[l >>> 8 & 255] ^ a[255 & u] ^ n[p++];
                    f = r[f >>> 24] ^ o[l >>> 16 & 255] ^ i[u >>> 8 & 255] ^ a[255 & d] ^ n[p++],
                        l = m,
                        u = g,
                        d = v
                }
                m = (s[l >>> 24] << 24 | s[u >>> 16 & 255] << 16 | s[d >>> 8 & 255] << 8 | s[255 & f]) ^ n[p++],
                    g = (s[u >>> 24] << 24 | s[d >>> 16 & 255] << 16 | s[f >>> 8 & 255] << 8 | s[255 & l]) ^ n[p++],
                    v = (s[d >>> 24] << 24 | s[f >>> 16 & 255] << 16 | s[l >>> 8 & 255] << 8 | s[255 & u]) ^ n[p++],
                    f = (s[f >>> 24] << 24 | s[l >>> 16 & 255] << 16 | s[u >>> 8 & 255] << 8 | s[255 & d]) ^ n[p++],
                    e[t] = m,
                    e[t + 1] = g,
                    e[t + 2] = v,
                    e[t + 3] = f
            },
            keySize: 8
        });
        e.AlocalStorage = t._createHelper(n)
    }();
    o.pad.ZeroPadding = {
        pad: function (e, t) {
            var n = 4 * t;
            e.clamp(),
                e.sigBytes += n - (e.sigBytes % n || n)
        },
        unpad: function (e) {
            for (var t = e.words, n = e.sigBytes - 1; !(t[n >>> 2] >>> 24 - n % 4 * 8 & 255);)
                n--;
            e.sigBytes = n + 1
        }
    }
    var codes = o.AlocalStorage.d(e, a, {
        iv: s,
        mode: o.mode.CBC,
        padding: o.pad.Pkcs7
    }).toString(o.enc.Utf8).toString();
    // console.log(codes);
    return codes;
}