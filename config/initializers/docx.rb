# Fix docx missed tabs bug

require 'zip'

module Zip
  class InputStream
    def sysread(length = nil, outbuf = '')
      @decompressor.read(length, outbuf).gsub('<w:tab/>', "<w:t>\t</w:t>")
    end
  end
end
