# This is the PRC configuration file for public releases of the game.
# It's rather similar to the dev PRC, but w/ some unneeded options removed.

# VFS for resources.
model-path resources
model-cache-models #f
model-cache-textures #f
vfs-mount phase_3.mf /
vfs-mount phase_3.5.mf /
vfs-mount phase_4.mf /
vfs-mount phase_5.mf /
vfs-mount phase_5.5.mf /
vfs-mount phase_6.mf /
vfs-mount phase_7.mf /
vfs-mount phase_8.mf /
vfs-mount phase_9.mf /
vfs-mount phase_10.mf /
vfs-mount phase_11.mf /
vfs-mount phase_12.mf /
vfs-mount phase_13.mf /
default-model-extension .bam

# RPC:
want-rpc-server #f
rpc-server-endpoint http://localhost:8080/

# DClass file:
dc-file dependencies/astron/dclass/empire.dc

# Client settings
window-title Toontown Empire
server-version Toontown Empire
build-version production
sync-video #f
want-dev #f
preload-avatars #t
texture-anisotropic-degree 16
icon-filename phase_3/etc/icon.ico
audio-library-name p3openal_audio
default-directnotify-level info
smooth-lag 0.4

# Core features:
want-pets #t
want-parties #t
want-cogdominiums #t
want-lawbot-cogdo #t
want-anim-props #t
want-game-tables #f
want-find-four #f
want-chinese-checkers #f
want-checkers #f
want-house-types #t
want-gifting #t
want-top-toons #f

# Chat:
want-whitelist #t
want-sequence-list #t

# Developer options:
show-population #t
want-instant-parties #f
gl-check-errors #t
want-extra-logs #f
want-instant-delivery #t
cogdo-pop-factor 1.5
cogdo-ratio 0.5
default-directnotify-level info

# In-game News:
want-news-tab #t
want-news-page #t

#want-mongo #t